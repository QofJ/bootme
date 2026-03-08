#!/usr/bin/env node

import { input, checkbox, confirm } from '@inquirer/prompts';
import { getDefaultInstallPath, getAutohotkeysDir } from '../utils.js';
import { scanAhkFiles, detectExistingFiles } from '../scanner.js';
import { installAhkFiles } from '../installer.js';

async function main() {
  console.log('\n🚀 AutoHotkey TUI Installer\n');

  // Step 1: Select installation path
  const defaultPath = getDefaultInstallPath();
  const installPath = await input({
    message: 'Select installation path:',
    default: defaultPath,
  });

  // Step 2: Scan and select files to install
  const availableFiles = scanAhkFiles();

  if (availableFiles.length === 0) {
    console.log('\n⚠️  No .ahk files found in autohotkeys directory.');
    console.log(`   Expected location: ${getAutohotkeysDir()}\n`);
    process.exit(0);
  }

  const selectedFiles = await checkbox({
    message: 'Select files to install:',
    choices: availableFiles.map(file => ({
      name: file,
      value: file,
      checked: true,
    })),
  });

  if (selectedFiles.length === 0) {
    console.log('\n⚠️  No files selected. Exiting.\n');
    process.exit(0);
  }

  // Step 3: Handle existing files
  const existingFiles = detectExistingFiles(installPath, selectedFiles);
  const skipFiles = [];

  if (existingFiles.length > 0) {
    console.log(`\n📁 Found ${existingFiles.length} existing file(s) in target directory.\n`);

    for (const file of existingFiles) {
      const shouldOverwrite = await confirm({
        message: `"${file}" already exists. Overwrite?`,
        default: false,
      });

      if (!shouldOverwrite) {
        skipFiles.push(file);
      }
    }
  }

  // Step 4: Confirm and install
  const filesToInstall = selectedFiles.filter(f => !skipFiles.includes(f));

  if (filesToInstall.length === 0) {
    console.log('\n⚠️  No files to install (all skipped). Exiting.\n');
    process.exit(0);
  }

  console.log('\n📦 Installation Summary:');
  console.log(`   Target: ${installPath}`);
  console.log(`   Files to install: ${filesToInstall.length}`);
  if (skipFiles.length > 0) {
    console.log(`   Files to skip: ${skipFiles.length}`);
  }

  const shouldProceed = await confirm({
    message: 'Proceed with installation?',
    default: true,
  });

  if (!shouldProceed) {
    console.log('\n❌ Installation cancelled.\n');
    process.exit(0);
  }

  // Execute installation
  console.log('\n⏳ Installing...\n');
  const result = installAhkFiles(selectedFiles, installPath, skipFiles);

  // Display results
  if (result.installed.length > 0) {
    console.log('✅ Successfully installed:');
    result.installed.forEach(f => console.log(`   - ${f}`));
  }

  if (result.skipped.length > 0) {
    console.log('⏭️  Skipped:');
    result.skipped.forEach(f => console.log(`   - ${f}`));
  }

  if (result.failed.length > 0) {
    console.log('❌ Failed:');
    result.failed.forEach(f => console.log(`   - ${f}`));
  }

  console.log('\n✨ Done!\n');
}

main().catch(error => {
  console.error('\n❌ Error:', error.message);
  process.exit(1);
});

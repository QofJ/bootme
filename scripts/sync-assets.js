#!/usr/bin/env node

/**
 * Sync .ahk files from assets/autohotkeys to src/bootme/assets/autohotkeys
 * Run this before publishing to ensure both npm and PyPI packages have the same files.
 */

import { cpSync, mkdirSync, existsSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const rootDir = join(__dirname, '..');

const sourceDir = join(rootDir, 'assets', 'autohotkeys');
const targetDir = join(rootDir, 'src', 'bootme', 'assets', 'autohotkeys');

// Ensure target directory exists
if (!existsSync(targetDir)) {
  mkdirSync(targetDir, { recursive: true });
}

// Copy all .ahk files
const files = readdirSync(sourceDir).filter(f => f.endsWith('.ahk'));

if (files.length === 0) {
  console.log('⚠️  No .ahk files found in', sourceDir);
  process.exit(1);
}

for (const file of files) {
  cpSync(join(sourceDir, file), join(targetDir, file));
  console.log(`✓ Copied ${file}`);
}

console.log(`\n✅ Synced ${files.length} file(s) to ${targetDir}`);

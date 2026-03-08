import { mkdirSync, copyFileSync, existsSync } from 'fs';
import { join } from 'path';
import { getAutohotkeysDir } from './utils.js';

/**
 * Ensure a directory exists, create if not
 * @param {string} dir - Directory path
 */
export function ensureDir(dir) {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

/**
 * Install a single AHK file to the target directory
 * @param {string} fileName - Name of the file to install
 * @param {string} targetDir - Target installation directory
 * @returns {boolean} Success status
 */
export function installAhkFile(fileName, targetDir) {
  const sourceDir = getAutohotkeysDir();
  const sourcePath = join(sourceDir, fileName);
  const targetPath = join(targetDir, fileName);

  try {
    ensureDir(targetDir);
    copyFileSync(sourcePath, targetPath);
    return true;
  } catch (error) {
    console.error(`Failed to install ${fileName}: ${error.message}`);
    return false;
  }
}

/**
 * Install multiple AHK files to the target directory
 * @param {string[]} files - Array of file names to install
 * @param {string} targetDir - Target installation directory
 * @param {string[]} skipFiles - Array of file names to skip
 * @returns {{ installed: string[], failed: string[], skipped: string[] }}
 */
export function installAhkFiles(files, targetDir, skipFiles = []) {
  const result = {
    installed: [],
    failed: [],
    skipped: []
  };

  const skipSet = new Set(skipFiles);

  for (const file of files) {
    if (skipSet.has(file)) {
      result.skipped.push(file);
      continue;
    }

    const success = installAhkFile(file, targetDir);
    if (success) {
      result.installed.push(file);
    } else {
      result.failed.push(file);
    }
  }

  return result;
}

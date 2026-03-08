import { readdirSync, existsSync } from 'fs';
import { join, basename } from 'path';
import { getAutohotkeysDir } from './utils.js';

/**
 * Scan all .ahk files in the autohotkeys directory
 * @returns {string[]} Array of .ahk file names
 */
export function scanAhkFiles() {
  const autohotkeysDir = getAutohotkeysDir();

  if (!existsSync(autohotkeysDir)) {
    return [];
  }

  const files = readdirSync(autohotkeysDir);
  return files.filter(file => file.endsWith('.ahk'));
}

/**
 * Detect which files already exist in the target directory
 * @param {string} targetDir - Target installation directory
 * @param {string[]} filesToInstall - Array of file names to check
 * @returns {string[]} Array of file names that already exist
 */
export function detectExistingFiles(targetDir, filesToInstall) {
  if (!existsSync(targetDir)) {
    return [];
  }

  return filesToInstall.filter(file => {
    const targetPath = join(targetDir, file);
    return existsSync(targetPath);
  });
}

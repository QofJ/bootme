import { homedir } from 'os';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

/**
 * Get the default AutoHotkey installation path
 * @returns {string} Default path (~/Documents/AutoHotkey)
 */
export function getDefaultInstallPath() {
  return join(homedir(), 'Documents', 'AutoHotkey');
}

/**
 * Get the autohotkeys source directory path
 * @returns {string} Path to autohotkeys directory
 */
export function getAutohotkeysDir() {
  return join(__dirname, '..', 'autohotkeys');
}

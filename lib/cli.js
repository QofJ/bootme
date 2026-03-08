#!/usr/bin/env node

import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { spawn } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const subcommand = process.argv[2];

const commands = {
  autohotkey: './commands/autohotkey.js',
};

function showHelp() {
  console.log(`
Usage: bootme <command>

Commands:
  autohotkey    Install AutoHotkey scripts

Options:
  -h, --help    Show this help message
`);
}

if (subcommand === '-h' || subcommand === '--help' || !subcommand) {
  showHelp();
  process.exit(0);
}

if (commands[subcommand]) {
  const child = spawn('node', [join(__dirname, commands[subcommand])], {
    stdio: 'inherit',
  });
  child.on('exit', (code) => process.exit(code));
} else {
  console.error(`Unknown command: ${subcommand}`);
  showHelp();
  process.exit(1);
}

#!/usr/bin/env node

import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { spawn } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));

const subcommand = process.argv[2];

if (subcommand === 'autohotkey') {
  const child = spawn('node', [join(__dirname, 'autohotkey.js')], {
    stdio: 'inherit'
  });
  child.on('exit', (code) => process.exit(code));
} else {
  console.log('Hello, world!');
}

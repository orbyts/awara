#!/usr/bin/env node
import {readFileSync} from 'node:fs';
import {schema, validate} from './index.js';
const [command, file] = process.argv.slice(2);
if (command === '--version') console.log('awara 0.0.0');
else if (command === 'schema') console.log(JSON.stringify(schema, null, 2));
else if (command === 'validate' && file && process.argv.length === 4) {
  try {
    const errors = validate(JSON.parse(readFileSync(file, 'utf8')));
    console.log(errors.length ? errors.join('\n') : 'Valid Awara recipe');
    process.exitCode = errors.length ? 1 : 0;
  } catch(e) { console.error(e.message); process.exitCode = 2; }
} else { console.error('Usage: awara validate FILE | schema | --version'); process.exitCode = 2; }

import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {validate} from './index.js';
for (const c of JSON.parse(readFileSync(new URL('../tests/cases.json', import.meta.url)))) {
  test(c.name, () => assert.equal(validate(c.recipe).length === 0, c.valid));
}

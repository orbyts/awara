import Ajv2020 from 'ajv/dist/2020.js';
import schema from './recipe.schema.json' with { type: 'json' };
const check = new Ajv2020({allErrors: true}).compile(schema);
export { schema };
export function validate(recipe) {
  check(recipe);
  return (check.errors ?? []).map(e => `${e.instancePath}: ${e.message}`);
}

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const canonical = new Set([
  'Blinded', 'Broken', 'Clumsy', 'Concealed', 'Confused', 'Controlled',
  'Cursebound', 'Dazzled', 'Deafened', 'Doomed', 'Drained', 'Dying',
  'Encumbered', 'Enfeebled', 'Fascinated', 'Fatigued', 'Fleeing', 'Friendly',
  'Frightened', 'Grabbed', 'Helpful', 'Hidden', 'Hostile', 'Immobilized',
  'Indifferent', 'Invisible', 'Observed', 'Off-Guard', 'Paralyzed',
  'Persistent Damage', 'Petrified', 'Prone', 'Quickened', 'Restrained',
  'Sickened', 'Slowed', 'Stunned', 'Stupefied', 'Unconscious', 'Undetected',
  'Unfriendly', 'Unnoticed', 'Wounded',
]);
const valued = new Set([
  'Clumsy', 'Cursebound', 'Doomed', 'Drained', 'Dying', 'Enfeebled',
  'Frightened', 'Sickened', 'Slowed', 'Stunned', 'Stupefied', 'Wounded',
]);
function readJson(file) {
  const source = fs.readFileSync(file, 'utf8');
  // Encounter+ accepts JSON5-style trailing commas in system definitions;
  // generated compendium records remain strict JSON.
  return JSON.parse(source.replace(/,\s*([}\]])/g, '$1'));
}

test('combat status menu uses canonical StatusEffect records', () => {
  const config = readJson(path.join(root, 'config.json'));
  assert.deepEqual(config.statusEffects.menuProvider, ['StatusEffect:condition']);
});

test('the 43 canonical Remaster conditions are picker-ready', () => {
  const packRoot = path.join(root, 'compendium', 'packs');
  const records = [];
  for (const source of fs.readdirSync(packRoot)) {
    const file = path.join(packRoot, source, 'conditions.json');
    if (fs.existsSync(file)) records.push(...readJson(file));
  }

  const picker = records.filter((record) => record.type === 'condition');
  assert.equal(picker.length, canonical.size);
  assert.deepEqual(new Set(picker.map((record) => record.name)), canonical);

  for (const record of picker) {
    assert.equal(record.reference, `/condition/${record.slug}`);
    assert.equal(record.icon, 'icons/conditions.png');
    assert.match(record.color, /^#[0-9A-F]{6}$/i);
    assert.doesNotMatch(record.descr, /\[[^\]]+\]\(\/[a-z-]+\/[^)\s]+\)/);
    assert.equal(record.data.duration, undefined);
    assert.equal(record.data.valued, valued.has(record.name));
    assert.equal(record.data.stage > 0, valued.has(record.name));
  }
});

test('the status-effect editor does not duplicate the built-in description field', () => {
  const form = readJson(path.join(root, 'forms', 'status-effect.json'));
  const fields = form.sections
    .flatMap((section) => section.fields || [])
  const customDescriptionFields = fields.filter((field) => field.attribute === 'descr');

  assert.equal(customDescriptionFields.length, 0);
});

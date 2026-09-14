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
const modifierCounts = new Map(Object.entries({
  Blinded: 1,
  Clumsy: 6,
  Confused: 1,
  Deafened: 1,
  Drained: 2,
  Dying: 4,
  Encumbered: 11,
  Enfeebled: 2,
  Fascinated: 18,
  Fatigued: 4,
  Frightened: 30,
  Grabbed: 1,
  'Off-Guard': 1,
  Paralyzed: 1,
  Petrified: 1,
  Prone: 1,
  Restrained: 1,
  Sickened: 30,
  Stupefied: 18,
  Unconscious: 4,
}));

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
    assert.equal(
      record.modifiers.length,
      modifierCounts.get(record.name) || 0,
      `${record.name} modifier count`,
    );
  }
});

test('relevant conditions use editable native modifier records', () => {
  const records = readJson(path.join(root, 'compendium', 'packs', 'player-core', 'conditions.json'));
  const conditions = new Map(records.map((record) => [record.name, record]));
  const modified = new Set(
    records.filter((record) => record.type === 'condition' && record.modifiers.length)
      .map((record) => record.name),
  );
  assert.deepEqual(modified, new Set(modifierCounts.keys()));

  for (const name of modified) {
    for (const modifier of conditions.get(name).modifiers) {
      assert.deepEqual(
        Object.keys(modifier).sort(),
        ['attribute', 'enabled', 'id', 'mode', 'name', 'scope', 'value'],
      );
      assert.match(modifier.id, /^[0-9A-F]{8}(?:-[0-9A-F]{4}){3}-[0-9A-F]{12}$/);
      assert.equal(modifier.enabled, true);
      assert.ok(['add', 'override'].includes(modifier.mode));
      assert.equal(modifier.scope, 'self');
      assert.match(modifier.attribute, /^data\.[A-Za-z0-9.]+$/);
      assert.match(modifier.value, /^-?\d+$/);
      assert.ok(modifier.name.length > 0);
    }
  }

  function values(condition, attribute) {
    return conditions.get(condition).modifiers
      .filter((modifier) => modifier.attribute === attribute)
      .map((modifier) => [modifier.mode, modifier.value]);
  }

  assert.deepEqual(values('Fatigued', 'data.ac.value'), [['add', '-1']]);
  assert.deepEqual(values('Off-Guard', 'data.ac.value'), [['add', '-2']]);
  assert.deepEqual(values('Blinded', 'data.perception'), [['add', '-4']]);
  assert.deepEqual(values('Deafened', 'data.perception'), [['add', '-2']]);
  assert.deepEqual(values('Encumbered', 'data.movement.walk'), [['add', '-10']]);
  assert.deepEqual(values('Petrified', 'data.ac.value'), [['override', '9']]);
  assert.deepEqual(values('Unconscious', 'data.ac.value'), [
    ['add', '-4'],
    ['add', '-2'],
  ]);
});

test('creature and character transforms consume every condition modifier path', () => {
  const records = readJson(path.join(root, 'compendium', 'packs', 'player-core', 'conditions.json'));
  const attributes = new Set(
    records.flatMap((record) => record.modifiers.map((modifier) => modifier.attribute)),
  );

  for (const entity of ['creature', 'character']) {
    const transform = readJson(path.join(root, 'views', 'transforms', `${entity}.json`));
    const patterns = transform.attributes.flatMap((group) => group.modifiers || []);
    for (const attribute of attributes) {
      const consumed = patterns.some((pattern) => {
        if (!pattern.startsWith('r/')) return pattern === attribute;
        if (pattern.endsWith('.*')) return attribute.startsWith(pattern.slice(2, -1));
        return false;
      });
      assert.equal(consumed, true, `${entity} does not consume ${attribute}`);
    }
  }
});

test('the status-effect editor does not duplicate the built-in description field', () => {
  const form = readJson(path.join(root, 'forms', 'status-effect.json'));
  const fields = form.sections
    .flatMap((section) => section.fields || [])
  const customDescriptionFields = fields.filter((field) => field.attribute === 'descr');

  assert.equal(customDescriptionFields.length, 0);
});

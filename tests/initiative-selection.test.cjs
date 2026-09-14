const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');

function readJson5(file) {
  const source = fs.readFileSync(file, 'utf8');
  return JSON.parse(source.replace(/,\s*([}\]])/g, '$1'));
}

test('system settings support global or per-creature initiative selection', () => {
  const settings = readJson5(path.join(root, 'forms', 'settings.json'));
  const combat = settings.sections.find((section) => section.title === 'Combat Tracker');
  const selector = combat.fields.find(
    (field) => field.attribute === 'combat.initiative.rollFormula'
  );
  const types = readJson5(path.join(root, 'types.json'));

  assert.equal(selector.type, 'picker');
  assert.equal(selector.attributeType, 'InitiativeRollFormula');
  assert.equal(selector.defaultValue, 'd20 + @entity.data.initiativeBonus');
  assert.equal(
    types.InitiativeRollFormula['d20 + @entity.data.initiativeBonus'],
    'Initiative.EachCreature'
  );
  assert.equal(
    types.InitiativeRollFormula['d20 + @entity.data.skills.stealth'],
    'Skill.Stealth'
  );
});

test('creature editor selects the statistic used by per-creature initiative', () => {
  const form = readJson5(path.join(root, 'forms', 'creature.json'));
  const fields = form.sections.flatMap((section) => section.fields || []);
  const selector = fields.find((field) => field.attribute === 'data.initiativeSkill');
  const types = readJson5(path.join(root, 'types.json'));
  const transform = readJson5(path.join(root, 'views', 'transforms', 'creature.json'));
  const formula = transform.attributes[0]['data.initiativeBonus'];

  assert.equal(selector.type, 'picker');
  assert.equal(selector.attributeType, 'InitiativeSkill');
  assert.equal(selector.defaultValue, 'perception');
  assert.equal(types.InitiativeSkill.perception, 'Creature.Perception');
  assert.equal(types.InitiativeSkill.deception, 'Skill.Deception');
  assert.match(formula, /data\.skills\[data\.initiativeSkill\]/);
  assert.match(formula, /data\.initiativeSkill in data\.skills/);
  assert.match(formula, /data\.perception/);
  assert.doesNotMatch(formula, /elsif/);
});

test('initiative configuration keeps the native Encounter+ roll formula', () => {
  const config = readJson5(path.join(root, 'config.json'));
  assert.equal(
    config.combat.initiative.rollFormula,
    'd20 + @entity.data.initiativeBonus'
  );
});

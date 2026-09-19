const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');

function readJson5(file) {
  const source = fs.readFileSync(file, 'utf8');
  return JSON.parse(source.replace(/,\s*([}\]])/g, '$1'));
}

test('system settings support global or per-combatant initiative selection', () => {
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
    'Initiative.EachCombatant'
  );
  assert.equal(
    types.InitiativeRollFormula['d20 + @entity.data.skills.stealth'],
    'Skill.Stealth'
  );
});

test('creature library entries do not store situational initiative choices', () => {
  const form = readJson5(path.join(root, 'forms', 'creature.json'));
  const fields = form.sections.flatMap((section) => section.fields || []);
  const types = readJson5(path.join(root, 'types.json'));

  assert.equal(fields.some((field) => field.attribute === 'data.initiativeSkill'), false);
  assert.equal(types.InitiativeSkill, undefined);
});

test('the status menu provides one temporary initiative choice for every skill', () => {
  const config = readJson5(path.join(root, 'config.json'));
  const types = readJson5(path.join(root, 'types.json'));
  const effects = readJson5(path.join(root, 'initiative-effects.json'));
  const skills = new Set(Object.keys(types.Skill));
  const expectedAttributes = {
    acrobatics: 'dex',
    arcana: 'int',
    athletics: 'str',
    crafting: 'int',
    deception: 'cha',
    diplomacy: 'cha',
    intimidation: 'cha',
    lore: 'int',
    medicine: 'wis',
    nature: 'wis',
    occultism: 'int',
    performance: 'cha',
    religion: 'wis',
    society: 'int',
    stealth: 'dex',
    survival: 'wis',
    thievery: 'dex',
  };

  assert.deepEqual(config.statusEffects.menuProvider, [
    'StatusEffect:initiative',
    'StatusEffect:condition',
  ]);
  assert.equal(effects.length, skills.size);
  assert.deepEqual(new Set(effects.map((effect) => effect.data.initiativeSkill)), skills);

  for (const effect of effects) {
    assert.equal(effect.kind, 'StatusEffect');
    assert.equal(effect.type, 'initiative');
    assert.equal(effect.attributes.license, 'Project-Code');
    assert.equal(
      effect.data.initiativeAttribute,
      expectedAttributes[effect.data.initiativeSkill]
    );
    assert.deepEqual(effect.modifiers, []);
    assert.equal(effect.icon, 'icons/conditions.png');
    assert.equal(effect.reference, undefined);
    assert.match(effect.descr, /Remove this effect to return to Perception\.$/);
  }
});

test('combatant effects choose initiative without changing the library entity', () => {
  for (const entity of ['creature', 'character']) {
    const transform = readJson5(path.join(root, 'views', 'transforms', `${entity}.json`));
    const formula = transform.attributes[0]['data.initiativeBonus'];

    assert.match(formula, /combatant\.effects/);
    assert.match(formula, /effect\.type == 'initiative'/);
    assert.match(formula, /effect\.data\.initiativeSkill in data\.skills/);
    assert.match(formula, /data\.skills\[effect\.data\.initiativeSkill\]/);
    assert.match(formula, /effect\.data\.initiativeAttribute in data\.attributes/);
    assert.match(formula, /data\.attributes\[effect\.data\.initiativeAttribute\]/);
    assert.match(formula, /forloop\.first/);
    assert.match(formula, /\{% empty %\}/);
    assert.match(formula, /data\.perception/);
    assert.doesNotMatch(formula, /data\.initiativeSkill and/);
    assert.doesNotMatch(formula, /set initiativeBonus/);
    assert.doesNotMatch(formula, /elsif/);
  }
});

test('initiative configuration keeps the native Encounter+ roll formula', () => {
  const config = readJson5(path.join(root, 'config.json'));
  assert.equal(
    config.combat.initiative.rollFormula,
    'd20 + @entity.data.initiativeBonus'
  );
});

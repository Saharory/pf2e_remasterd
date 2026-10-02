{% if data.perception %}
**{{'Creature.Perception'|l}}** [{{data.perception|signed}}](roll "{{'Creature.Perception'|l}}"){% if data.senses %}; {{data.senses}}{% endif %}
{% endif %}

{% if data.recallKnowledge.dc %}
[**{{'Creature.RecallKnowledge'|l}}**](/action/recall-knowledge-player-core){% if data.recallKnowledge.subject %}—[{{data.recallKnowledge.subject|map: 'Trait'}}](/trait/{{data.recallKnowledge.subject}}){% endif %}{% if data.recallKnowledge.skills %} ({% for skill in data.recallKnowledge.skills %}[{{skill|map: 'Skill'}}](/rule/{{skill}}-skill-player-core){% if not forloop.last %}, {% endif %}{% endfor %}){% endif %}: DC {{data.recallKnowledge.dc}}
{% endif %}

{% if data.languages %}
[**{{'Creature.Languages'|l}}**](/rule/languages-rules-2080) {% for language in data.languages %}[{{language|map: 'Language'}}](/language/{{language}}){% if not forloop.last %}, {% endif %}{% endfor %}{% if data.languagesDetails %}; {{data.languagesDetails}}{% endif %}
{% endif %}

{% if data.skills %}
[**{{'Creature.Skills'|l}}**](/rule/skills-rules-2276) {% for key, value in data.skills %}[{{ key|map: 'Skill' }}](/rule/{{key}}-skill-player-core) [{{value|signed}}](roll "{{ key|map: 'Skill' }}"){% if not forloop.last %}, {% endif %}{% endfor %}
{% endif %}

{% if data.loreSkills %}
[**Lore**](/rule/lore-skill-player-core) {% for skill in data.loreSkills %}{{skill.name}} [{{skill.value|signed}}](roll "{{skill.name}}"){% if not forloop.last %}, {% endif %}{% endfor %}
{% endif %}

**{{'Attribute.STR'|l|capitalize}}** [{{data.attributes.str|default: 0|signed}}](roll "{{'strength'|map: 'Attribute'}}") **{{'Attribute.DEX'|l|capitalize}}** [{{data.attributes.dex|default: 0|signed}}](roll "{{'dexterity'|map: 'Attribute'}}") **{{'Attribute.CON'|l|capitalize}}** [{{data.attributes.con|default: 0|signed}}](roll "{{'constitution'|map: 'Attribute'}}") **{{'Attribute.INT'|l|capitalize}}** [{{data.attributes.int|default: 0|signed}}](roll "{{'intelligence'|map: 'Attribute'}}") **{{'Attribute.WIS'|l|capitalize}}** [{{data.attributes.wis|default: 0|signed}}](roll "{{'wisdom'|map: 'Attribute'}}") **{{'Attribute.CHA'|l|capitalize}}** [{{data.attributes.cha|default: 0|signed}}](roll "{{'charisma'|map: 'Attribute'}}")

{% if data.items %}
**{{'Creature.Items'|l}}** {{data.items}}
{% endif %}

{% for ability in data.abilities.interaction %}
{% include "ability.md" %}
{% endfor %}

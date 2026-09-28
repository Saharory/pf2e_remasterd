{% if data.perception %}
**{{'Creature.Perception'|l}}** [{{data.perception|signed}}](roll "{{'Creature.Perception'|l}}"){% if data.senses %}; {{data.senses}}{% endif %}
{% endif %}

{% if data.recallKnowledge.dc %}
[**{{'Creature.RecallKnowledge'|l}}**](/action/recall-knowledge-player-core) DC {{data.recallKnowledge.dc}}{% if data.recallKnowledge.skills %} ({% for skill in data.recallKnowledge.skills %}{{skill|map: 'Skill'}}{% if not forloop.last %}, {% endif %}{% endfor %}){% endif %}
{% endif %}

{% if data.languages %}
**{{'Creature.Languages'|l}}** {% for language in data.languages %}{{language|map: 'Language'}}{% if not forloop.last %}, {% endif %}{% endfor %}
{% endif %}

{% if data.skills %}
**{{'Creature.Skills'|l}}** {% for key, value in data.skills %}{{ key|map: 'Skill' }} [{{value|signed}}](roll "{{ key|map: 'Skill' }}"), {% endfor %}
{% endif %}

{% if data.loreSkills %}
**Lore** {% for skill in data.loreSkills %}{{skill.name}} [{{skill.value|signed}}](roll "{{skill.name}}"), {% endfor %}
{% endif %}

**{{'Attribute.STR'|l|capitalize}}** [{{data.attributes.str|default: 0|signed}}](roll "{{'strength'|map: 'Attribute'}}") **{{'Attribute.DEX'|l|capitalize}}** [{{data.attributes.dex|default: 0|signed}}](roll "{{'dexterity'|map: 'Attribute'}}") **{{'Attribute.CON'|l|capitalize}}** [{{data.attributes.con|default: 0|signed}}](roll "{{'constitution'|map: 'Attribute'}}") **{{'Attribute.INT'|l|capitalize}}** [{{data.attributes.int|default: 0|signed}}](roll "{{'intelligence'|map: 'Attribute'}}") **{{'Attribute.WIS'|l|capitalize}}** [{{data.attributes.wis|default: 0|signed}}](roll "{{'wisdom'|map: 'Attribute'}}") **{{'Attribute.CHA'|l|capitalize}}** [{{data.attributes.cha|default: 0|signed}}](roll "{{'charisma'|map: 'Attribute'}}")

{% if data.items %}
**{{'Creature.Items'|l}}** {{data.items}}
{% endif %}

{% for ability in data.abilities.interaction %}
{% include "ability.md" %}
{% endfor %}

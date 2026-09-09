**{{'Common.AC'|l}}** {{data.ac.value}}{% if data.ac.details %} ({{data.ac.details}}){% endif %} ; {% if data.saves.fortitude != nil %}**{{'SavingThrow.Fort'|l}}** [{{data.saves.fortitude|signed}}](roll "{{'SavingThrow.Fort'|l}}/save"), {% endif %}{% if data.saves.reflex != nil %}**{{'SavingThrow.Ref'|l}}** [{{data.saves.reflex|signed}}](roll "{{'SavingThrow.Ref'|l}}/save"), {% endif %}{% if data.saves.will != nil %}**{{'SavingThrow.Wil'|l}}** [{{data.saves.will|signed}}](roll "{{'SavingThrow.Wil'|l}}/save"){% endif %}{% if data.saves.details %} ; {{data.saves.details}}{% endif %}

**{{'Common.HP'|l}}** {{data.hp.value}} ;{% if data.hp.details %} {{data.hp.details|lowercase}} ;{% endif %}{% if data.immunities %} **{{'Creature.Immunities'|l}}** {{data.immunities|lowercase|join:', '}} ;{% endif %}{% if data.weaknesses %} **{{'Creature.Weaknesses'|l}}** {% for key, value in data.weaknesses %}{{ key|map: 'Damage'|lowercase }} {{value}}{% if not forloop.last %}, {% endif %}{% endfor %} ;{% endif %}{% if data.resistances %} **{{'Creature.Resistances'|l}}** {% for key, value in data.resistances %}{{ key|map: 'Damage'|lowercase }} {{value}}{% if not forloop.last %}, {% endif %}{% endfor %}{% endif %}

{% for ability in data.abilities.defensive %}
{% include "ability.md" %}
{% endfor %}

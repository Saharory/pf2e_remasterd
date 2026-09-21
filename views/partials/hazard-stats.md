{% if data.complexity %}**{{data.complexity|capitalize}} hazard**
{% endif %}
{% if data.stealth != nil and data.stealth != 0 %}**Stealth** [{{data.stealth|signed}}](roll "Stealth"){% if data.stealthDetails %} {{data.stealthDetails}}{% endif %}
{% endif %}
{% if data.disable %}**Disable** {{data.disable}}
{% endif %}
{% if data.hp.value > 0 %}---

{% if data.ac.value > 0 %}**{{'Common.AC'|l}}** {{data.ac.value}}{% if data.ac.details %} ({{data.ac.details}}){% endif %}; {% endif %}**{{'Common.HP'|l}}** {{data.hp.value}}{% if data.hp.details %} ({{data.hp.details}}){% endif %}{% if data.hardness > 0 %}; **{{'Item.Hardness'|l}}** {{data.hardness}}{% endif %}

{% if data.saves.fortitude != 0 and data.saves.fortitude != nil %}**{{'SavingThrow.Fort'|l}}** [{{data.saves.fortitude|signed}}](roll "{{'SavingThrow.Fort'|l}}/save") {% endif %}{% if data.saves.reflex != 0 and data.saves.reflex != nil %}**{{'SavingThrow.Ref'|l}}** [{{data.saves.reflex|signed}}](roll "{{'SavingThrow.Ref'|l}}/save") {% endif %}{% if data.saves.will != 0 and data.saves.will != nil %}**{{'SavingThrow.Wil'|l}}** [{{data.saves.will|signed}}](roll "{{'SavingThrow.Wil'|l}}/save"){% endif %}

{% endif %}
{% for ability in data.attacks %}{% include "attack.md" %}
{% endfor %}
{% for ability in data.abilities %}{% include "ability.md" %}
{% endfor %}
{% if data.routine %}**Routine** {{data.routine}}
{% endif %}
{% if data.reset %}**Reset** {{data.reset}}
{% endif %}

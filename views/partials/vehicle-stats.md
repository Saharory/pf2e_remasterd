{% if data.price %}**{{'Item.Price'|l}}** {{data.price}}
{% endif %}
{% if data.space.long %}**Space** {{data.space.long}} feet long × {{data.space.wide}} feet wide × {{data.space.high}} feet high
{% endif %}
{% if data.crew %}**Crew** {{data.crew}}{% endif %}{% if data.passengers %}; **Passengers** {{data.passengers}}{% endif %}

{% if data.pilotingCheck %}**Piloting Check** {{data.pilotingCheck}}
{% endif %}
{% if data.speed %}**{{'Common.Speed'|l}}** {{data.speed}}
{% endif %}
{% if data.hp.value > 0 %}---

{% if data.ac.value > 0 %}**{{'Common.AC'|l}}** {{data.ac.value}}{% if data.ac.details %} ({{data.ac.details}}){% endif %}; {% endif %}**{{'Common.HP'|l}}** {{data.hp.value}}{% if data.hp.details %} ({{data.hp.details}}){% endif %}{% if data.hardness > 0 %}; **{{'Item.Hardness'|l}}** {{data.hardness}}{% endif %}{% if data.fortitude != nil %}; **{{'SavingThrow.Fort'|l}}** [{{data.fortitude|signed}}](roll "{{'SavingThrow.Fort'|l}}/save"){% endif %}
{% endif %}
{% if data.collisionDC > 0 %}**Collision** DC {{data.collisionDC}}{% if data.collisionDamage %}; **{{'Common.Damage'|l}}** {{data.collisionDamage|roll: 'Collision', 'damage'}}{% endif %}
{% endif %}
{% for ability in data.abilities %}{% include "ability.md" %}
{% endfor %}

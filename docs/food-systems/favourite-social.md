# Favourite And Social Bonuses

Favourite food and cooked-by metadata are player-data systems. They are separate from recipe matching, but they can combine with food properties at eating time.

## Favourite Food

Players choose a favourite with `/hl favourite`. Eating that custom food grants:

| Effect | Duration | Strength |
| --- | --- | --- |
| Regeneration | 30 seconds | I |
| Saturation | 15 seconds | II |
| Luck | 60 seconds | I |

The favourite check runs after food-property effects. A property-stacked favourite therefore applies both sets of behavior.

## Cooked By

When a player crafts edible output, Heirloom can store the crafter UUID. Later, favourite-food checks can reward the cook with a short regeneration effect if somebody else eats the favourite food they made.

## Affinity

`AFFINITY` also reads cooked-by metadata. If the food was cooked by someone else, it grants regeneration to the eater. If that same food is also the eater's favourite, the regeneration amplifier is increased.

## Data Storage

Player RPG data is saved under `plugins/Heirloom/playerdata/`. Favourite choice and mastery are stored per player.

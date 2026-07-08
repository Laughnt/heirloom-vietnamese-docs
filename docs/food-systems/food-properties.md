# Food Properties

Food properties are gameplay tags stored on the item. They are not just wiki categories: when you eat the item, Heirloom loops over every stored property and applies the matching behavior.

## Where Properties Come From

A property can be added by a recipe action, usually `ADD_METADATA` with key `food_property`, or it can already exist on an ingredient. When a recipe finishes, Heirloom starts with properties already on the output, then adds every property found on every input item. The result is stored back on the output and shown in lore.

That means properties can stack through recipe chains.

## Worked Example: Powerful Pancakes

1. Make jam in the Boiling Pot with `CHORUS_FRUIT`. The jam rule adds `CHORUS`.
2. Make another jam with `GOLDEN_APPLE`. The jam rule adds `GOLDEN`.
3. Use property-bearing jam as a pancake topping in the Frying Pan. Pancakes inherit the jam's stored properties.
4. Eat the pancakes. The food applies every stored food property, then any JSON-defined effects, then favourite-food effects if pancakes are your favourite.

In bundled data, honey pancakes add honey naming, quality, and bottle return behavior. Honey does not add `SWEET` to pancakes unless a recipe or custom item explicitly stores `SWEET` as a food property. Server owners can add that behavior with recipe actions.

## Exact Property Effects

| Property | Effect when eaten |
| --- | --- |
| `GLOWING` | Glowing I for 30 seconds, beacon-style sound/message |
| `GOLDEN` | Regeneration II for 5 seconds and Absorption I for 2 minutes |
| `CHORUS` | Attempts a safe random teleport, like chorus fruit |
| `SWEET` | Speed I and Haste I for 10 seconds |
| `SPICY` | Fire Resistance I for 20 seconds, plus 1 second of visual fire |
| `COLD` | Slowness I for 5 seconds and Resistance II for 10 seconds |
| `ENERGIZING` | Speed II, Haste II, and Jump Boost I for 30 seconds |
| `NOURISHING` | Saturation III for 5 seconds |
| `HEALING` | Instant Health II |
| `AFFINITY` | If cooked by another player, Regeneration I for 10 seconds; Regeneration II if it is also your favourite food |
| `SOBERING` | If Distillery is loaded and inebriation is enabled, drains drunkenness by the configured amount, default 15 |

## What Players See

The recipe browser preview can show food-property lore based on the selected ingredients. Finished items also carry the property lore. If the final food is placed as a serving food, the placed block stores the properties too, so bites can still apply the behavior.

## Server Owner Pattern

Use properties for intentional power chains. For example, a server could make maple syrup add `SWEET`, then pancakes made with `GOLDEN` jam and syrup would carry both the inherited jam property and the syrup property.

```json
{
  "type": "ADD_METADATA",
  "key": "food_property",
  "value": "SWEET"
}
```

Avoid relying on hidden balance. If a food should heal, sober, teleport, energize, or become a strong favourite-food candidate, put that behavior in the recipe or ingredient data.

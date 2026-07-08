# Custom Recipes

Recipes define a station, output, processing time, ingredients, actions, and optional rules. The output can be changed by base actions, rule actions, inherited input metadata, and quality logic.

## Minimum Recipe

```json
{
  "id": "SWEET_PANCAKES",
  "station": "FRYING_PAN",
  "output": "PANCAKES",
  "processing_time": 160,
  "ingredients": [
    { "type": "REQUIRED", "max": 1, "options": [{ "custom_item": "BAG_OF_FLOUR" }] },
    { "type": "REQUIRED", "max": 1, "options": [{ "item": "EGG" }] },
    { "type": "OPTIONAL", "max": 1, "options": [{ "item": "HONEY_BOTTLE" }] }
  ],
  "actions": [
    { "type": "SET_PROPERTY", "key": "NAME", "value": "Sweet Pancakes" },
    { "type": "ADD_METADATA", "key": "food_property", "value": "SWEET" }
  ]
}
```

## Advanced Pattern: Property Chain

Put properties on intermediate ingredients when you want players to build stronger food through multiple steps. For example, jam can get `CHORUS` from chorus fruit, then pancakes inherit that property when the jam is used as a topping.

## Common Rule Actions

- `SET_PROPERTY` with key `NAME`: changes display name.
- `ADD_METADATA` with key `food_property`: adds a food property that can be inherited and applied when eaten.
- `SET_RETURN_ITEM`: returns a container when crafting completes.
- `SET_CONSUME_RETURN`: returns a container after eating.
- `SET_VISUAL_ITEM`: swaps to a provider-neutral visual variant.
- `ADD_QUALITY` and `SET_QUALITY`: tune output quality.

## Common Mistakes

- Using `SET_PROPERTY` for `food_property`; bundled property recipes use `ADD_METADATA` for inherited food properties.
- Putting a custom item in `item` instead of `custom_item`.
- Forgetting that optional slots default to `0-max`, so rules must handle the missing-input case.
- Editing JSON and testing only `/hl give`; recipe actions and inheritance only appear when the recipe is crafted.

## How To Test

Run `/hl reload`, search the recipe, craft every branch you changed, and inspect lore. For inheritance tests, craft the intermediate ingredient first, then use that exact item in the next recipe.

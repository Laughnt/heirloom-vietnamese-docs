# Custom Foods

Custom foods are defined in JSON under `custom_items` arrays. A custom food defines the item players can hold; recipes define how players make it.

## Minimum Edible Food

```json
{
  "id": "GOLDEN_PANCAKE",
  "name": "Golden Pancake",
  "base_material": "PLAYER_HEAD",
  "texture": "http://textures.minecraft.net/texture/...",
  "edible": true,
  "food_value": 8,
  "saturation": 6.0,
  "consume_seconds": 1.4,
  "animation": "EAT",
  "visual_id": "GOLDEN_PANCAKE"
}
```

## Advanced Fields To Know

- `consume_return`: gives an item back after eating.
- `placeable_servings`: makes the food placeable and eaten in servings.
- `feast`: enables shared-feast behavior.
- `effects`: applies explicit potion effects when eaten.
- `visual_id`: lets Nexo or ItemsAdder replace the visual without changing recipes.

## Common Mistakes

- Defining an item but never adding a recipe for it.
- Using a pretty `name` but forgetting the stable uppercase `id` used in recipes.
- Expecting a property effect without adding a recipe action or stored property.
- Using provider-specific visual IDs instead of stable Heirloom visual IDs.

## How To Test

Use `/hl give <id>` to inspect the item definition, then craft it through the intended recipe to inspect inherited quality, properties, and returns.

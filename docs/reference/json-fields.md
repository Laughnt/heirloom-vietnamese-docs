# JSON Field Reference

## Custom Item Fields

| Field | Meaning |
| --- | --- |
| `id` | Stable uppercase item ID |
| `name` | Display name |
| `base_material` | Vanilla base material |
| `texture` | Player-head texture URL |
| `edible` | Whether the item can be consumed |
| `food_value` | Hunger restored |
| `saturation` | Saturation restored |
| `consume_seconds` | Consume duration |
| `animation` | `EAT` or `DRINK` style animation |
| `effects` | Potion effects |
| `visual_id` | Provider-neutral visual lookup key |
| `consume_return` | Item returned after consumption or recipe use |
| `placeable_servings` | Cake-like serving count |
| `feast` | Enables feast participant behavior |

## Recipe Fields

| Field | Meaning |
| --- | --- |
| `id` | Stable recipe ID |
| `station` | Cooking station |
| `output` | Main output item |
| `weighted_outputs` | Chance-based output list |
| `processing_time` | Ticks |
| `ingredients` | Required/optional slots |
| `actions` | Always-applied output changes |
| `rules` | Conditional output changes |

## Crop Fields

| Field | Meaning |
| --- | --- |
| `id` | Crop ID |
| `item_id` | Item used for planting/harvest |
| `plant_type` | Physical crop behavior |
| `growth` | Timing, scale, stages |
| `planting` | Valid blocks and permissions |
| `textures` | Growing/ripe display textures |
| `harvest` | Drops, sounds, replant, quality chance |

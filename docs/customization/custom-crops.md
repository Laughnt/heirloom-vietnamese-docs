# Custom Crops

Crop JSON defines plant type, growth behavior, planting rules, textures, and harvest drops.

## Minimum Crop Shape

A crop needs an item ID, plant type, growth settings, planting rules, textures, and harvest rules. Use an existing crop close to your desired behavior as the starting point: lettuce for ground crops, tomato for vines, rice for aquatic crops, corn for tall crops.

## Important Sections

- `growth`: duration, variance, stages, and scale.
- `planting`: valid blocks, item consumption, and permission.
- `textures`: growing and ripe display textures.
- `harvest`: drops, bonus drops, replanting, sounds, and quality chance.

## Design Choices

Choose a plant type based on physical behavior. A tomato-like crop should be a vine because it needs a wall. A rice-like crop should be aquatic because the water requirement is part of gameplay. Do not use a display offset to fake a crop type that has different block rules.

## Common Mistakes

- Enabling world generation for a vine crop without natural wall positions.
- Giving aquatic crops to players before they know the water placement rule.
- Adding bonus drops that require Fortune, then testing with an unenchanted tool.
- Forgetting crop permissions when planting works for admins but not players.

## How To Test

Plant it, wait or speed up growth, harvest it, confirm drops, confirm replanting, then test in a protected region with a normal player.

# Distillery Brewing Flow

## Main Flow

1. Mash or stomp ingredients.
2. Branch by ingredient profile.
3. Ferment fruit must, or boil grain wort before fermentation.
4. Distill stronger spirits when the drink type supports it.
5. Inspect traits, ABV, and quality.

## Fruit Vs Grain

Fruit must is ready for fermentation after crushing. Grain wort needs the Boiling Pot first, then fermentation. This is the most common player confusion, so use `/hld stats <item>` and item lore when teaching the addon.

## Metadata Matters

Distillery drinks preserve metadata through custom output handlers. Ingredients, traits, ABV, and quality are part of the item identity, not just the display name.

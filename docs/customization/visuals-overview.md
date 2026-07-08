# Visual Integrations Overview

Heirloom works without a resource pack by using vanilla materials and player-head textures. Optional providers can replace that presentation.

## Provider-Neutral Flow

1. Item definitions declare `visual_id`.
2. Recipes can call `SET_VISUAL_ITEM`.
3. `VisualItemResolver` asks registered providers for that visual.
4. If no provider has it, Heirloom falls back to the normal item.

This keeps recipe data independent from Nexo or ItemsAdder.

## Practical Rule

Use Heirloom item IDs and visual IDs as stable public names. Let Nexo or ItemsAdder map those names to models. Do not bake a provider namespace into a recipe unless you want that recipe to stop being portable.

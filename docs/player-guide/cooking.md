# Cooking Basics

Heirloom cooking is physical. You build a station in the world, add visible ingredients, process the station, then either collect the result or keep using that result as part of a recipe chain.

## Station Loop Example

## The Station Loop

1. Build the correct station shape.
2. Right-click with ingredients to place them on the station.
3. Empty your hand and right-click to begin processing.
4. Wait for the station effects and progress to finish.
5. Left-click to collect the output, or keep the output in the station flow if the next recipe uses it.

## Chains Are The Point

Many foods are not one-step crafts. Flour can become dough, dough can become bread or pancakes, rice can become cooked rice and then a meal, and jam can become a topping that carries properties into another food. When a recipe says it wants `JAM`, it means the actual item you made, including quality, creator data, consume returns, and food properties.

## What Changes A Result

A finished food can be changed by recipe rules, optional ingredients, inherited properties, quality, and visual actions. That is why two foods with the same output ID can have different names, lore, textures, or effects.

## Container Returns

Some recipes and foods return buckets or bottles. There are two common cases:

* Craft return: the station gives something back when the recipe completes.
* Consume return: eating the food gives something back afterward, such as a bottle from jam.

## Common Failure Cases

* The station shape is wrong, so Heirloom never treats the block as a station.
* The ingredient is the wrong form, such as `WHEAT` instead of `BAG_OF_FLOUR`.
* The recipe belongs to another station or addon.
* An optional ingredient matched the base recipe but not the rule you expected.
* A protection plugin cancelled interaction in the region.

Use `/hl search <ingredient>` when stuck. It is usually faster than guessing the next station.

# Frying Pan

## Build

Build a Frying Pan with a `HEAVY_WEIGHTED_PRESSURE_PLATE` on top of a `FURNACE`.

## Core Loop

The Frying Pan handles eggs, bacon, pancakes, fried rice, and other fast heated foods.

## How Recipes Behave Here

The Frying Pan is fast heat. It handles eggs, bacon, pancakes, fried rice, and other foods where toppings and optional ingredients change the final item. This station is one of the clearest places to see inherited properties: a special jam used as a pancake topping can carry `CHORUS`, `GOLDEN`, or other properties into the finished pancakes.

## Common Chains

* Eggs and bacon prove the station works with simple vanilla inputs.
* `PANCAKES` accept flour/cornmeal, eggs, milk, and optional toppings such as `JAM`, honey, or chocolate.
* `FRIED_RICE` and similar recipes usually depend on rice being cooked first at the Boiling Pot.

## Good First Recipes

Cook a plain egg, then pancakes, then pancakes with a custom jam. Compare the lore: the topping can change name, quality, return behavior, and inherited food properties.

## What Can Go Wrong

The recipe can be valid but still produce a plain-looking result if the optional ingredient did not match the rule you expected. For example, bundled honey pancakes add honey naming, quality, and bottle return behavior; they do not add `SWEET` unless a recipe or custom ingredient explicitly stores that food property.

## Recipes

| Recipe                                                                    | Output                                                                     | Inputs              | Source |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------- | ------ |
| [`BACON`](../recipes/default-recipes.md#recipe-bacon)                     | [BACON](../../recipes/default-recipes/#recipe-bacon)                       |                     | Core   |
| [`EGGS_AND_BACON`](../recipes/default-recipes.md#recipe-eggs-and-bacon)   | [EGGS\_AND\_BACON](../../recipes/default-recipes/#recipe-eggs-and-bacon)   | oror1-2             | Core   |
| [`FALAFEL`](../recipes/default-recipes.md#recipe-falafel)                 | [FALAFEL](../../recipes/default-recipes/#recipe-falafel)                   | oror1-2             | World  |
| [`FISH_AND_CHIPS`](../recipes/default-recipes.md#recipe-fish-and-chips-2) | [FISH\_AND\_CHIPS](../../recipes/default-recipes/#recipe-fish-and-chips-2) |                     | Core   |
| [`FLATBREAD`](../recipes/default-recipes.md#recipe-flatbread)             | [FLATBREAD](../../recipes/default-recipes/#recipe-flatbread)               |                     | Core   |
| [`FRENCH_TOAST`](../recipes/default-recipes.md#recipe-french-toast)       | [FRENCH\_TOAST](../../recipes/default-recipes/#recipe-french-toast)        | ororor              | Core   |
| [`FRIED_EGG`](../recipes/default-recipes.md#recipe-fried-egg)             | [FRIED\_EGG](../../recipes/default-recipes/#recipe-fried-egg)              | oror1-3             | Core   |
| [`FRIED_RICE`](../recipes/default-recipes.md#recipe-fried-rice)           | [FRIED\_RICE](../../recipes/default-recipes/#recipe-fried-rice)            | oror0-10-10-10-1    | Core   |
| [`GRILLED_CHEESE`](../recipes/default-recipes.md#recipe-grilled-cheese)   | [GRILLED\_CHEESE](../../recipes/default-recipes/#recipe-grilled-cheese)    | or                  | Core   |
| [`HAMBURGER`](../recipes/default-recipes.md#recipe-hamburger)             | [HAMBURGER](../../recipes/default-recipes/#recipe-hamburger)               | oror0-10-10-1       | Core   |
| [`OMELETTE`](../recipes/default-recipes.md#recipe-omelette)               | [OMELETTE](../../recipes/default-recipes/#recipe-omelette)                 | oror1-30-10-10-10-1 | Core   |
| [`PANCAKES`](../recipes/default-recipes.md#recipe-pancakes)               | [PANCAKES](../../recipes/default-recipes/#recipe-pancakes)                 | ororororor0-3       | Core   |
| [`POPCORN`](../recipes/default-recipes.md#recipe-popcorn)                 | [POPCORN](../../recipes/default-recipes/#recipe-popcorn)                   |                     | Core   |
| [`TACO`](../recipes/default-recipes.md#recipe-taco-2)                     | [TACO](../../recipes/default-recipes/#recipe-taco-2)                       | oror0-10-10-1       | Core   |

## Troubleshooting

If a recipe does not match, use `/hl search <ingredient>` and confirm every ingredient belongs at this station.

See the full [recipe index](../recipes/default-recipes.md) for ingredient links, processing time, recipe rules, and output actions.

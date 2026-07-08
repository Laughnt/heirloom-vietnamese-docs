# Mixing Bowl

## Build

Build a Mixing Bowl with a `FLOWER_POT` on any `STRIPPED_` log, wood, stem, hyphae, or bamboo block.

## Core Loop

The Mixing Bowl handles dough, mixing, cold preparation, and Cafe grinding steps.

## How Recipes Behave Here

The Mixing Bowl is for combining, folding, grinding, and cold prep. It often creates neutral intermediates that later become powerful when cooked elsewhere: dough, batter, cream, plant protein, and Cafe grinding steps all live here.

## Common Chains

* Flour and liquids become `DOUGH`, then the Oven or Frying Pan finishes the dish.
* Cafe uses grinding-style recipes for tea leaves, matcha chances, and other drink prep.
* Mixed ingredients can inherit dietary and food-property data from custom inputs, so the bowl is often where a server-owner recipe starts carrying metadata forward.

## Good First Recipes

Use the bowl for dough and cream before testing more advanced recipe chains. These are easier to debug because their ingredients are obvious.

## What Can Go Wrong

If a recipe looks right but does not match, check whether the input wants a custom item such as `BAG_OF_FLOUR` rather than vanilla `WHEAT`. For server owners, this station is a good place to test optional slots because it makes failures easy to see before cooking time is involved.

## Recipes

| Recipe                                                                                  | Output                                                                             | Inputs                                 | Source  |
| --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | -------------------------------------- | ------- |
| [`BUTTER_RECIPE`](../recipes/default-recipes.md#recipe-butter-recipe)                   | [BUTTER](../../recipes/default-recipes/#recipe-butter-recipe)                      |                                        | Core    |
| [`COOKING_OIL_CORN`](../recipes/default-recipes.md#recipe-cooking-oil-corn)             | [COOKING\_OIL](../../recipes/default-recipes/#recipe-cooking-oil-corn)             | 1-2                                    | Core    |
| [`COOKING_OIL_SUNFLOWER`](../recipes/default-recipes.md#recipe-cooking-oil-sunflower)   | [COOKING\_OIL](../../recipes/default-recipes/#recipe-cooking-oil-sunflower)        | 1-4                                    | Core    |
| [`DOUGH`](../recipes/default-recipes.md#recipe-dough)                                   | [DOUGH](../../recipes/default-recipes/#recipe-dough)                               | ororor0-10-10-10-10-1                  | Core    |
| [`EGGNOG`](../recipes/default-recipes.md#recipe-eggnog)                                 | [EGGNOG](../../recipes/default-recipes/#recipe-eggnog)                             | 1-2                                    | Festive |
| [`GRIND_BLACK_TEA_LEAVES`](../recipes/default-recipes.md#recipe-grind-black-tea-leaves) | [BLACK\_TEA\_LEAVES](../../recipes/default-recipes/#recipe-grind-black-tea-leaves) | 1-2                                    | Cafe    |
| [`GRIND_GREEN_TEA_LEAVES`](../recipes/default-recipes.md#recipe-grind-green-tea-leaves) | [DRIED\_GREEN\_TEA](../../recipes/default-recipes/#recipe-grind-green-tea-leaves)  | ororororororororor1-2                  | Cafe    |
| [`GRIND_MATCHA_POWDER`](../recipes/default-recipes.md#recipe-grind-matcha-powder)       | [DRIED\_GREEN\_TEA](../../recipes/default-recipes/#recipe-grind-matcha-powder)     |                                        | Cafe    |
| [`HEAVY_CREAM_RECIPE`](../recipes/default-recipes.md#recipe-heavy-cream-recipe)         | [HEAVY\_CREAM](../../recipes/default-recipes/#recipe-heavy-cream-recipe)           |                                        | Core    |
| [`ICE_CREAM`](../recipes/default-recipes.md#recipe-ice-cream)                           | [ICE\_CREAM](../../recipes/default-recipes/#recipe-ice-cream)                      | ororororor0-1ororororororororororor0-4 | Core    |
| [`MAKE_OAT_MILK`](../recipes/default-recipes.md#recipe-make-oat-milk)                   | [OAT\_MILK](../../recipes/default-recipes/#recipe-make-oat-milk)                   | 1-2                                    | Cafe    |
| [`PLANT_PROTEIN`](../recipes/default-recipes.md#recipe-plant-protein)                   | [PLANT\_PROTEIN](../../recipes/default-recipes/#recipe-plant-protein)              | ororor                                 | Core    |
| [`SALAD`](../recipes/default-recipes.md#recipe-salad)                                   | [SALAD](../../recipes/default-recipes/#recipe-salad)                               | 1-2ororororororororor0-4ororor0-1or0-1 | Core    |
| [`VINEGAR`](../recipes/default-recipes.md#recipe-vinegar)                               | [VINEGAR](../../recipes/default-recipes/#recipe-vinegar)                           |                                        | Core    |

## Troubleshooting

Use a shovel-style tool for mixing interactions. In survival, use a pickaxe if you intend to break the station cleanly.

See the full [recipe index](../recipes/default-recipes.md) for ingredient links, processing time, recipe rules, and output actions.

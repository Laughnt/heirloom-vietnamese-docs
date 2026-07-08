# Oven

## Build

Build an Oven with a `STONE_PRESSURE_PLATE` on top of a `SMOKER`.

## Core Loop

The Oven handles baking, roasting, drying, and some chain steps such as bread, pizza, and coffee roasting.

## How Recipes Behave Here

The Oven is the long-form heat station. It is where raw prep becomes shelf-stable or baked food: dough becomes bread, flat dough becomes pizza, wet coffee cherries become roast beans, and some addon chains use it as the first serious processing step.

## Common Chains

* `BAG_OF_FLOUR` -> `DOUGH` -> bread, pizza, pancakes, waffles, doughnuts, and pastry-style recipes.
* Cafe coffee cherries roast through light, medium, and dark beans before they become espresso drinks.
* Recipes with `SET_RETURN_ITEM` can give containers back after the craft, so check the output and your inventory before assuming a bucket or bottle vanished.

## Good First Recipes

Start with bread or baked potato-style recipes before testing pizzas and addon chains. They prove the station structure works without requiring several intermediate ingredients.

## What Can Go Wrong

If a recipe never starts, first confirm the station is the smoker plus stone pressure plate pair. If the station works but a recipe does not match, search the exact output or ingredient with `/hl search <query>`; many baked foods need an intermediate Heirloom item rather than the raw vanilla ingredient.

## Recipes

| Recipe                                                                                                            | Output                                                                                  | Inputs                | Source  |
| ----------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------- | ------- |
| [`BAKE_MUFFIN`](../recipes/default-recipes.md#recipe-bake-muffin)                                                 | [MUFFIN](../../recipes/default-recipes/#recipe-bake-muffin)                             | ororororor0-1         | Cafe    |
| [`BEEF_WELLINGTON`](../recipes/default-recipes.md#recipe-beef-wellington)                                         | [BEEF\_WELLINGTON](../../recipes/default-recipes/#recipe-beef-wellington)               |                       | Core    |
| [`BREAD`](../recipes/default-recipes.md#recipe-bread)                                                             | [BREAD](../../recipes/default-recipes/#recipe-bread)                                    |                       | Core    |
| [`CHOCOLATE`](../recipes/default-recipes.md#recipe-chocolate)                                                     | [CHOCOLATE](../../recipes/default-recipes/#recipe-chocolate)                            |                       | Core    |
| [`CHRISTMAS_HAM`](../recipes/default-recipes.md#recipe-christmas-ham)                                             | [CHRISTMAS\_HAM](../../recipes/default-recipes/#recipe-christmas-ham)                   | 2                     | Festive |
| [`GINGERBREAD`](../recipes/default-recipes.md#recipe-gingerbread)                                                 | [GINGERBREAD](../../recipes/default-recipes/#recipe-gingerbread)                        |                       | Festive |
| [`KEBAB`](../recipes/default-recipes.md#recipe-kebab)                                                             | [KEBAB](../../recipes/default-recipes/#recipe-kebab)                                    | oror0-2               | World   |
| [`LASAGNA`](../recipes/default-recipes.md#recipe-lasagna)                                                         | [LASAGNA](../../recipes/default-recipes/#recipe-lasagna)                                | or0-10-1              | Core    |
| [`MAKE_LEAF_LITTER`](../recipes/default-recipes.md#recipe-make-leaf-litter)                                       | [LEAF\_LITTER](../../recipes/default-recipes/#recipe-make-leaf-litter)                  | ororororororororor1-3 | Cafe    |
| [`PIE`](../recipes/default-recipes.md#recipe-pie)                                                                 | [PIE](../../recipes/default-recipes/#recipe-pie)                                        | ororororor            | Core    |
| [`PIZZA`](../recipes/default-recipes.md#recipe-pizza)                                                             | [PIZZA](../../recipes/default-recipes/#recipe-pizza)                                    | orororororor0-4       | Core    |
| [`ROAST_COFFEE_CHERRY`](../recipes/default-recipes.md#recipe-roast-coffee-cherry)                                 | [COFFEE\_BEANS\_LIGHT](../../recipes/default-recipes/#recipe-roast-coffee-cherry)       | 1-3                   | Cafe    |
| [`ROAST_DARK_COFFEE_BEANS_TO_CHARCOAL`](../recipes/default-recipes.md#recipe-roast-dark-coffee-beans-to-charcoal) | [CHARCOAL](../../recipes/default-recipes/#recipe-roast-dark-coffee-beans-to-charcoal)   | 1-3                   | Cafe    |
| [`ROAST_LIGHT_COFFEE_BEANS`](../recipes/default-recipes.md#recipe-roast-light-coffee-beans)                       | [COFFEE\_BEANS\_MEDIUM](../../recipes/default-recipes/#recipe-roast-light-coffee-beans) | 1-3                   | Cafe    |
| [`ROAST_MEDIUM_COFFEE_BEANS`](../recipes/default-recipes.md#recipe-roast-medium-coffee-beans)                     | [COFFEE\_BEANS\_DARK](../../recipes/default-recipes/#recipe-roast-medium-coffee-beans)  | 1-3                   | Cafe    |
| [`ROAST_TURKEY`](../recipes/default-recipes.md#recipe-roast-turkey)                                               | [ROAST\_TURKEY](../../recipes/default-recipes/#recipe-roast-turkey)                     | or                    | Festive |
| [`SALT_RECIPE`](../recipes/default-recipes.md#recipe-salt-recipe)                                                 | [SALT](../../recipes/default-recipes/#recipe-salt-recipe)                               |                       | Core    |
| [`SHEPHERDS_PIE`](../recipes/default-recipes.md#recipe-shepherds-pie)                                             | [SHEPHERDS\_PIE](../../recipes/default-recipes/#recipe-shepherds-pie)                   | 0-1                   | Core    |
| [`TACO`](../recipes/default-recipes.md#recipe-taco)                                                               | [TACO](../../recipes/default-recipes/#recipe-taco)                                      | orororororor0-3       | Core    |
| [`WAFFLES`](../recipes/default-recipes.md#recipe-waffles)                                                         | [WAFFLES](../../recipes/default-recipes/#recipe-waffles)                                | ororororor0-3         | Core    |

## Troubleshooting

If the station does not activate, confirm the plate is directly above a smoker and that the clicked block is the plate.

See the full [recipe index](../recipes/default-recipes.md) for ingredient links, processing time, recipe rules, and output actions.

# Cutting Board

## Build

Build a Cutting Board with any wooden pressure plate on any `STRIPPED_` block.

## Core Loop

The Cutting Board handles prep work such as flour, pasta, minced ingredients, and sliced recipe steps.

## How Recipes Behave Here

The Cutting Board is prep work: chopping, slicing, mincing, and turning raw ingredients into precise recipe components. It is intentionally not a generic table; many recipes need the prepared form before another station accepts them.

## Common Chains

* `WHEAT` can become flour-style ingredients used by dough and batter chains.
* Meat and plant alternatives can become minced or sliced components for later meals.
* Pasta and similar prep items are made here before being boiled or cooked.

## Good First Recipes

Start with flour or pasta prep. Those recipes teach the difference between vanilla ingredients and Heirloom intermediate items.

## What Can Go Wrong

Use the correct physical station: wooden pressure plate on a stripped block. If a food chain seems blocked, search the output you expected; the missing step is often a Cutting Board ingredient rather than the final station.

## Recipes

| Recipe                                                                              | Output                                                                              | Inputs                           | Source  |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------- | ------- |
| [`BLT`](../recipes/default-recipes.md#recipe-blt)                                   | [BLT](../../recipes/default-recipes/#recipe-blt)                                    | oror                             | Core    |
| [`CORNMEAL`](../recipes/default-recipes.md#recipe-cornmeal)                         | [CORNMEAL](../../recipes/default-recipes/#recipe-cornmeal)                          |                                  | Core    |
| [`DRY_PASTA`](../recipes/default-recipes.md#recipe-dry-pasta)                       | [DRY\_PASTA](../../recipes/default-recipes/#recipe-dry-pasta)                       |                                  | Core    |
| [`FLOUR`](../recipes/default-recipes.md#recipe-flour)                               | [BAG\_OF\_FLOUR](../../recipes/default-recipes/#recipe-flour)                       |                                  | Core    |
| [`GINGERBREAD_HOUSE`](../recipes/default-recipes.md#recipe-gingerbread-house)       | [GINGERBREAD\_HOUSE](../../recipes/default-recipes/#recipe-gingerbread-house)       | 1-3or0-2                         | Festive |
| [`MINCED_MEAT_BEEF`](../recipes/default-recipes.md#recipe-minced-meat-beef)         | [MINCED\_MEAT](../../recipes/default-recipes/#recipe-minced-meat-beef)              | oror                             | Core    |
| [`SUSHI`](../recipes/default-recipes.md#recipe-sushi)                               | [SUSHI](../../recipes/default-recipes/#recipe-sushi)                                | orororor                         | Core    |
| [`SUSHI_ROLL`](../recipes/default-recipes.md#recipe-sushi-roll)                     | [SUSHI\_ROLL](../../recipes/default-recipes/#recipe-sushi-roll)                     | ororor                           | World   |
| [`VALENTINES_CHOCOLATE`](../recipes/default-recipes.md#recipe-valentines-chocolate) | [VALENTINES\_CHOCOLATE](../../recipes/default-recipes/#recipe-valentines-chocolate) | orororororororororororororororor | Festive |

## Troubleshooting

Use sword or axe-style tools for chopping interactions. Non-wood pressure plates are reserved for other stations or ignored.

See the full [recipe index](../recipes/default-recipes.md) for ingredient links, processing time, recipe rules, and output actions.

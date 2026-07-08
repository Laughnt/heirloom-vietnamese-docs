# Boiling Pot

## Build

Build a Boiling Pot with a `CAULDRON` or `WATER_CAULDRON` over a `CAMPFIRE` or `SOUL_CAMPFIRE`.

## Core Loop

The Boiling Pot handles wet recipes, soups, cheese, rice, pasta, and recipes that return buckets or bottles.

## How Recipes Behave Here

The Boiling Pot is the liquid and simmering station. It handles soups, rice, pasta, cheese, jam, wet ingredient conversions, and recipes that care about buckets or bottles. It is also where property stacking becomes easy to understand: jam can become an ingredient in later foods while keeping the food properties created from its fruit.

## Common Chains

* Fruit + sugar + bottle -> `JAM`; glow berries, golden apples, and chorus fruit can add food properties to the jam.
* `RICE` + water -> `COOKED_RICE`, which then feeds sushi and fried rice chains.
* Milk bucket -> `CHEESE`, and milk plus vinegar can produce the alternate cheese path.
* Distillery grain wort uses the Boiling Pot before fermentation.

## Good First Recipes

Try `COOKED_RICE`, `CHEESE`, then `JAM`. Those three cover water inputs, bucket returns, bottle returns, and property-carrying ingredients.

## What Can Go Wrong

A bucket can be either a normal Minecraft interaction or a recipe ingredient. If you are testing a recipe, interact normally with the station and avoid vanilla cauldron habits. If the output keeps the wrong flavor or property, inspect the recipe rules: properties come from matching ingredient rules and from inherited input data.

## Recipes

| Recipe                                                                    | Output                                                                    | Inputs        | Source  |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------- | ------- |
| [`CANDY_APPLE`](../recipes/default-recipes.md#recipe-candy-apple)         | [CANDY\_APPLE](../../recipes/default-recipes/#recipe-candy-apple)         | or1-2         | Festive |
| [`CANDY_CORN`](../recipes/default-recipes.md#recipe-candy-corn)           | [CANDY\_CORN](../../recipes/default-recipes/#recipe-candy-corn)           | 1-2           | Festive |
| [`CANNED_TOMATOES`](../recipes/default-recipes.md#recipe-canned-tomatoes) | [CANNED\_TOMATOES](../../recipes/default-recipes/#recipe-canned-tomatoes) |               | Core    |
| [`CHEESE`](../recipes/default-recipes.md#recipe-cheese)                   | [CHEESE](../../recipes/default-recipes/#recipe-cheese)                    |               | Core    |
| [`CHEESE`](../recipes/default-recipes.md#recipe-cheese-2)                 | [CHEESE](../../recipes/default-recipes/#recipe-cheese-2)                  |               | Core    |
| [`CHICKEN_CURRY`](../recipes/default-recipes.md#recipe-chicken-curry)     | [CHICKEN\_CURRY](../../recipes/default-recipes/#recipe-chicken-curry)     | orororor1-3   | World   |
| [`CHOCOLATE_EGG`](../recipes/default-recipes.md#recipe-chocolate-egg)     | [CHOCOLATE\_EGG](../../recipes/default-recipes/#recipe-chocolate-egg)     |               | Festive |
| [`COOKED_RICE`](../recipes/default-recipes.md#recipe-cooked-rice)         | [COOKED\_RICE](../../recipes/default-recipes/#recipe-cooked-rice)         | 0-1           | Core    |
| [`DOUGHNUT`](../recipes/default-recipes.md#recipe-doughnut)               | [DOUGHNUT](../../recipes/default-recipes/#recipe-doughnut)                | 0-1oror0-1    | Core    |
| [`FISH_AND_CHIPS`](../recipes/default-recipes.md#recipe-fish-and-chips)   | [FISH\_AND\_CHIPS](../../recipes/default-recipes/#recipe-fish-and-chips)  | oror          | Core    |
| [`FRIED_CHICKEN`](../recipes/default-recipes.md#recipe-fried-chicken)     | [FRIED\_CHICKEN](../../recipes/default-recipes/#recipe-fried-chicken)     | or            | Core    |
| [`FRIES`](../recipes/default-recipes.md#recipe-fries)                     | [FRIES](../../recipes/default-recipes/#recipe-fries)                      | 1-20-1        | Core    |
| [`JAM`](../recipes/default-recipes.md#recipe-jam)                         | [JAM](../../recipes/default-recipes/#recipe-jam)                          | ororororor1-3 | Core    |
| [`MAC_AND_CHEESE`](../recipes/default-recipes.md#recipe-mac-and-cheese)   | [MAC\_AND\_CHEESE](../../recipes/default-recipes/#recipe-mac-and-cheese)  | 0-10-1        | Core    |
| [`MASHED_POTATOES`](../recipes/default-recipes.md#recipe-mashed-potatoes) | [MASHED\_POTATOES](../../recipes/default-recipes/#recipe-mashed-potatoes) | 20-1          | Core    |
| [`PASTA_BOLOGNESE`](../recipes/default-recipes.md#recipe-pasta-bolognese) | [PASTA\_BOLOGNESE](../../recipes/default-recipes/#recipe-pasta-bolognese) | or            | Core    |
| [`TOMATO_SOUP`](../recipes/default-recipes.md#recipe-tomato-soup)         | [TOMATO\_SOUP](../../recipes/default-recipes/#recipe-tomato-soup)         | 0-1           | Core    |

## Troubleshooting

Water buckets are recipe ingredients for some recipes. Avoid sneak-right-clicking when you mean to add the bucket as an ingredient, because sneak interaction may allow vanilla cauldron behavior.

See the full [recipe index](../recipes/default-recipes.md) for ingredient links, processing time, recipe rules, and output actions.

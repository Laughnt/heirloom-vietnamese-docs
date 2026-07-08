# Barista Machine

## Build

Build a Barista Machine with an `IRON_TRAPDOOR` above `QUARTZ_STAIRS`. The Cafe addon must be installed and registered.

## Core Loop

The Barista Machine pulls espresso, tea, cocoa, boba, iced drinks, and milk-based drinks from Cafe ingredients.

## How Recipes Behave Here

The Barista Machine is Cafe's drink assembly station. Earlier Cafe steps happen on core stations: cherries roast in the Oven, leaves and powders use prep stations, and the Barista Machine turns those prepared ingredients into drinks.

## Common Chains

* Coffee cherry -> light beans -> medium beans -> dark beans -> espresso -> americano, latte, cappuccino, flat white, mocha, or iced coffee.
* Leaves -> dried or ground tea ingredients -> green tea, black tea, sweet tea, matcha latte, or boba tea.
* Milk bucket and oat milk variants often change names, returns, and dietary behavior.

## Good First Recipes

Pull `ESPRESSO`, then make `AMERICANO`, then a milk drink. That proves the chain, the station, and container returns.

## What Can Go Wrong

The station only registers when Cafe is installed. If the trapdoor and quartz stairs act like normal blocks, confirm the Cafe jar loaded, `/hlc help` works, and Cafe recipes appear in `/hl search cafe`.

## Recipes

| Recipe                                                                        | Output                                                                   | Inputs       | Source |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ------------ | ------ |
| [`BREW_AMERICANO`](../recipes/default-recipes.md#recipe-brew-americano)       | [AMERICANO](../../recipes/default-recipes/#recipe-brew-americano)        |              | Cafe   |
| [`BREW_BLACK_TEA`](../recipes/default-recipes.md#recipe-brew-black-tea)       | [TEA\_DRINK](../../recipes/default-recipes/#recipe-brew-black-tea)       | 0-1          | Cafe   |
| [`BREW_BOBA_TEA`](../recipes/default-recipes.md#recipe-brew-boba-tea)         | [BOBA\_TEA](../../recipes/default-recipes/#recipe-brew-boba-tea)         | ororor0-1    | Cafe   |
| [`BREW_CAPPUCCINO`](../recipes/default-recipes.md#recipe-brew-cappuccino)     | [CAPPUCCINO](../../recipes/default-recipes/#recipe-brew-cappuccino)      | or2          | Cafe   |
| [`BREW_ESPRESSO`](../recipes/default-recipes.md#recipe-brew-espresso)         | [ESPRESSO](../../recipes/default-recipes/#recipe-brew-espresso)          | or           | Cafe   |
| [`BREW_FLAT_WHITE`](../recipes/default-recipes.md#recipe-brew-flat-white)     | [FLAT\_WHITE](../../recipes/default-recipes/#recipe-brew-flat-white)     | 2or          | Cafe   |
| [`BREW_GREEN_TEA`](../recipes/default-recipes.md#recipe-brew-green-tea)       | [TEA\_DRINK](../../recipes/default-recipes/#recipe-brew-green-tea)       | 0-1          | Cafe   |
| [`BREW_HOT_COCOA`](../recipes/default-recipes.md#recipe-brew-hot-cocoa)       | [HOT\_COCOA](../../recipes/default-recipes/#recipe-brew-hot-cocoa)       | or1-2oror0-1 | Cafe   |
| [`BREW_ICED_COFFEE`](../recipes/default-recipes.md#recipe-brew-iced-coffee)   | [ICED\_COFFEE](../../recipes/default-recipes/#recipe-brew-iced-coffee)   |              | Cafe   |
| [`BREW_LATTE`](../recipes/default-recipes.md#recipe-brew-latte)               | [LATTE](../../recipes/default-recipes/#recipe-brew-latte)                | or           | Cafe   |
| [`BREW_MATCHA_LATTE`](../recipes/default-recipes.md#recipe-brew-matcha-latte) | [MATCHA\_LATTE](../../recipes/default-recipes/#recipe-brew-matcha-latte) | or           | Cafe   |
| [`BREW_MOCHA`](../recipes/default-recipes.md#recipe-brew-mocha)               | [MOCHA](../../recipes/default-recipes/#recipe-brew-mocha)                | or           | Cafe   |

## Troubleshooting

If the station acts like normal blocks, confirm HeirloomCafe loaded and `/hlc help` works.

See the full [recipe index](../recipes/default-recipes.md) for ingredient links, processing time, recipe rules, and output actions.

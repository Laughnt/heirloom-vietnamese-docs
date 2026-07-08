# Dietary Properties

Dietary labels use a blacklist model. A recipe is assumed to satisfy a property unless one of its ingredients violates that property.

| Property | Display | Meaning | Implies |
| --- | --- | --- | --- |
| `VEGAN` | Vegan | Contains no animal products | `VEGETARIAN` |
| `VEGETARIAN` | Vegetarian | Contains no meat or fish |  |
| `GLUTEN_FREE` | Gluten-Free | Contains no gluten |  |

## How Calculation Works

When a recipe is previewed or crafted, Heirloom checks the selected ingredients. Vanilla ingredients are compared against dietary config. Custom ingredients can already carry stored dietary data, so a later recipe does not need to know every raw ingredient that originally created them.

## Inheritance Example

If a custom sauce was made with milk, and that sauce is later used in a sandwich, the sandwich should not become vegan just because the sandwich recipe only sees `SAUCE`. Stored dietary data keeps that history attached to the ingredient.

## Hierarchy

`hierarchy_rules` hide weaker labels when a stronger label is present. Bundled data treats `VEGAN` as implying `VEGETARIAN`, so vegan foods do not need to show both labels.

## Contains Lines

The `contains_settings` block controls "Contains:" lore. Use it for practical warnings, not just marketing labels. It is most useful for common allergens, roleplay restrictions, or server-specific diet rules.

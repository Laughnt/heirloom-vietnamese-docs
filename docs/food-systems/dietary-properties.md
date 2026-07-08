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

## Example: Adding Kosher Or Halal

You can add server-specific dietary rules the same way the bundled file defines `VEGAN`, `VEGETARIAN`, and `GLUTEN_FREE`. The important idea is that a property describes what is allowed, and its `violators` list describes what breaks that rule.

For example, a simple halal-style rule might blacklist pork materials and pork-based custom foods:

```json
"HALAL": {
  "display_name": "Halal",
  "description": "Contains no server-defined non-halal ingredients",
  "violators": {
    "items": [
      "PORKCHOP",
      "COOKED_PORKCHOP"
    ],
    "custom_items": [
      "BACON",
      "CHRISTMAS_HAM"
    ]
  }
}
```

A simple kosher-style rule can use the same structure:

```json
"KOSHER": {
  "display_name": "Kosher",
  "description": "Contains no server-defined non-kosher ingredients",
  "violators": {
    "items": [
      "PORKCHOP",
      "COOKED_PORKCHOP"
    ],
    "custom_items": [
      "BACON",
      "CHRISTMAS_HAM"
    ]
  }
}
```

After adding those entries under `dietary_properties`, reload and test a few chains. If `BACON` is made from `PORKCHOP`, the bacon will not receive `HALAL` or `KOSHER`. If that bacon is later used in `EGGS_AND_BACON`, `BLT`, or a custom burger, the finished food also will not receive those properties because custom ingredients carry their stored dietary data forward.

!!! note
    Heirloom enforces the rules you configure; it does not decide real-world religious law. If your server also wants to treat alcohol, shellfish, meat-and-dairy combinations, or specific addon drinks as disallowed, add those vanilla or custom item IDs to the appropriate `violators` lists and test the recipe chains players actually use.

## Hierarchy

`hierarchy_rules` hide weaker labels when a stronger label is present. Bundled data treats `VEGAN` as implying `VEGETARIAN`, so vegan foods do not need to show both labels.

## Contains Lines

The `contains_settings` block controls "Contains:" lore. Use it for practical warnings, not just marketing labels. It is most useful for common allergens, roleplay restrictions, or server-specific diet rules.

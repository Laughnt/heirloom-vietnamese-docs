# Favourite Food

Favourite food is a personal RPG feature. You choose one custom food, then get extra effects whenever you eat that food ID.

## Command

```text
/hl favourite
```

Aliases:

```text
/hl favorite
/hl fav
```

## What You Get

Eating your favourite food applies:

| Effect | Duration | Strength |
| --- | --- | --- |
| Regeneration | 30 seconds | I |
| Saturation | 15 seconds | II |
| Luck | 60 seconds | I |

These effects are added after normal food-property effects. If your favourite food is also a property-stacked food, both systems apply.

## Why It Matters

A plain favourite is useful. A favourite with inherited properties is stronger. For example, pancakes made with `GOLDEN` and `CHORUS` jam can apply those property effects, then the favourite-food package if pancakes are your selected favourite.

## Social Cooking

Heirloom stores cooked-by data on edible outputs. If somebody else cooked your favourite food, the favourite check can reward the cook with a short regeneration effect. The `AFFINITY` food property also reads cooked-by data and becomes stronger when the food is also your favourite.

## Server Notes For Players

If `/hl favourite` is unavailable, ask staff whether `heirloom.favourite` is granted. The feature is permission-gated so servers can decide whether it is part of default progression.

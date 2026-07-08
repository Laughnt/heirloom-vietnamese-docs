# Corn

| Field       | Value                                     |
| ----------- | ----------------------------------------- |
| Item        | [`CORN`](../reference/items.md#item-corn) |
| Plant type  | `TALL_PLANT`                              |
| Base growth | 480 seconds                               |
| Stages      | 5                                         |
| Permission  | `heirloom.crop.corn`                      |
| Replants    | `yes`                                     |

## Planting

Valid blocks: `GRASS_BLOCK`, `DIRT`, `COARSE_DIRT`, `PODZOL`, `ROOTED_DIRT`

Use the crop item on the correct block or face. If the crop has a permission, the player must have that node before planting.

## Harvest

Main drops: `CORN` 1-2.

If the crop keeps `replant_after_harvest` enabled, right-click harvest resets it to an early stage. Breaking the plant is treated as destruction, not a full harvest.

## Notes For Admins

Edit this crop in `crops.json` or the relevant addon crop file. Growth scale, stage count, valid blocks, sounds, drop chances, quality chance, and permission nodes are all data-driven.

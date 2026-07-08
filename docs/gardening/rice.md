# Rice

| Field       | Value                                     |
| ----------- | ----------------------------------------- |
| Item        | [`RICE`](../reference/items.md#item-rice) |
| Plant type  | `AQUATIC`                                 |
| Base growth | 360 seconds                               |
| Stages      | 4                                         |
| Permission  | `heirloom.crop.rice`                      |
| Replants    | `yes`                                     |

## Planting

Valid blocks: `DIRT`, `CLAY`, `MUD`, `GRAVEL`, `SAND`

Use the crop item on the correct block or face. If the crop has a permission, the player must have that node before planting.

## Harvest

Main drops: `RICE` 2-4.

If the crop keeps `replant_after_harvest` enabled, right-click harvest resets it to an early stage. Breaking the plant is treated as destruction, not a full harvest.

## Notes For Admins

Edit this crop in `crops.json` or the relevant addon crop file. Growth scale, stage count, valid blocks, sounds, drop chances, quality chance, and permission nodes are all data-driven.

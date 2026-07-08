# Tomato

<figure class="hl-figure">
  <img src="../../images/gardening/tomato.webp" alt="Tomato crop growing as a vine.">
  <figcaption>Tomato crop growing as a vine.</figcaption>
</figure>

| Field | Value |
| --- | --- |
| Item | [`TOMATO`](../reference/items.md#item-tomato) |
| Plant type | `VINE` |
| Base growth | 420 seconds |
| Stages | 4 |
| Permission | `heirloom.crop.tomato` |
| Replants | `yes` |

## Planting

Valid blocks: see crop JSON

Use the crop item on the correct block or face. If the crop has a permission, the player must have that node before planting.

## Harvest

Main drops: `TOMATO` 1-2.

If the crop keeps `replant_after_harvest` enabled, right-click harvest resets it to an early stage. Breaking the plant is treated as destruction, not a full harvest.

## Notes For Admins

Edit this crop in `crops.json` or the relevant addon crop file. Growth scale, stage count, valid blocks, sounds, drop chances, quality chance, and permission nodes are all data-driven.

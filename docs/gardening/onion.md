# Onion

<figure class="hl-figure">
  <img src="../../images/gardening/onion.webp" alt="Onion crop planted as an allium-style ground crop.">
  <figcaption>Onion crop planted as an allium-style ground crop.</figcaption>
</figure>

| Field | Value |
| --- | --- |
| Item | [`ONION`](../reference/items.md#item-onion) |
| Plant type | `ALLIUM` |
| Base growth | 360 seconds |
| Stages | 4 |
| Permission | `heirloom.crop.onion` |
| Replants | `yes` |

## Planting

Valid blocks: `GRASS_BLOCK`, `DIRT`, `COARSE_DIRT`, `PODZOL`, `ROOTED_DIRT`

Use the crop item on the correct block or face. If the crop has a permission, the player must have that node before planting.

## Harvest

Main drops: `ONION` 1-3.

If the crop keeps `replant_after_harvest` enabled, right-click harvest resets it to an early stage. Breaking the plant is treated as destruction, not a full harvest.

## Notes For Admins

Edit this crop in `crops.json` or the relevant addon crop file. Growth scale, stage count, valid blocks, sounds, drop chances, quality chance, and permission nodes are all data-driven.

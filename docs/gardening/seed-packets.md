# Seed Packets

Seed packets are custom items that roll weighted seeds when opened. They are useful when you want survival discovery without requiring every crop to drop from grass.

| Packet | Description | Drops | Weighted contents |
| --- | --- | --- | --- |
| `TEMPERATE_SEED_PACKET` | Contains seeds suited for temperate climates | 3-6 | `LETTUCE` (25), `CORN` (20), `TOMATO` (20), `ONION` (20), `WHEAT_SEEDS` (8), `BEETROOT_SEEDS` (4), `CARROT` (2), `POTATO` (1) |
| `TROPICAL_SEED_PACKET` | Contains seeds suited for tropical and exotic climates | 3-5 | `RICE` (40), `MELON_SEEDS` (20), `PUMPKIN_SEEDS` (20), `COCOA_BEANS` (15), `BAMBOO` (5) |

Players open packets by using the item. If their inventory is full, extra seeds drop nearby.

## Design Advice

Use seed packets for starter kits, market crates, quest rewards, and rare biome crops. Keep the drop count small if packets are common, otherwise a single packet can skip the early farming loop.

# Wild Discovery And Loot

`seed_acquisition.json` controls non-command crop discovery.

## Grass Drops

Grass drops use a base chance plus biome modifiers. The bundled config makes lettuce and onion common in plains/meadows, tomato more common in forests, corn more common in plains/savanna, and rice more common in swamp/jungle-style areas.

## Chest Loot

Village, farm, dungeon, mineshaft, and temple loot tables can receive Heirloom crop items or seed packets. The chance is per generated chest, not a guarantee for every structure.

## World Generation

Natural patches are placed in new chunks only. Ground crops are the safest candidates. Vine crops need walls, and aquatic crops need water placement, so test those carefully before enabling broad worldgen.

!!! warning
    World generation and chest loot only affect newly generated or newly filled content. Use commands, seed packets, or custom events if you need to seed old worlds.

# Cafe Configuration

Cafe writes editable resources to `plugins/HeirloomCafe/`:

- `custom_items-cafe.json`
- `crops-cafe.json`
- `recipes-cafe.json`
- `config.yml`
- `lang/en.yml`

Cafe unregisters and re-registers its addon-owned items, crops, and recipes on reload callbacks so the recipe browser can refresh.

## Test After Changes

After recipe edits, run `/hl reload`, search for `cafe`, then test one coffee chain and one tea chain. That catches both core-station prep and Barista Machine assembly.

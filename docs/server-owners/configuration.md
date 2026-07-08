# Configuration

Core files live in `plugins/Heirloom/` after first startup.

| File | Purpose |
| --- | --- |
| `config.yml` | License key and locale |
| `custom_items.json` | Core item definitions |
| `recipes.json` | Core recipes |
| `crops.json` | Core crops |
| `dietary_properties.json` | Diet labels and hierarchy |
| `seed_acquisition.json` | Seed packets, grass drops, loot, world patches |
| `advancements.json` | Advancement definitions |
| `enchantment_integrations.json` | EcoEnchants and compatible enchantment keys |
| `lang/<locale>.yml` | Locale files |

Run `/hl reload` after supported JSON and language changes. Restart after jar, dependency, or large visual-pack changes.

# EcoEnchants Integration

Heirloom reads enchantment integration data from `enchantment_integrations.json` and resolves registered Bukkit enchantments by namespaced key.

## Bundled EcoEnchants Hooks

| Purpose | Keys | Behavior |
| --- | --- | --- |
| Force replant | `ecoenchants:replant`, `ecoenchants:replenish` | Crop resets after harvest even when it would normally be removed |
| Fortune bonus | `ecoenchants:prospector` | Adds +1 effective Fortune per enchantment level |

## How This Affects Players

A replant enchantment makes farming smoother but still respects whether the crop is mature and harvestable. A Fortune bonus improves configured drop rolls; it does not invent drops that the crop JSON never defines.

## Server Owner Notes

You can add other enchantment keys in the same `namespace:name` format. After editing, reload and harvest a mature test crop with the enchanted tool to confirm the integration is detected.

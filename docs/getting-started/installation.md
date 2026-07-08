# Installation

Heirloom is a Paper plugin for modern Minecraft 1.21 servers. Install the core plugin first, then add optional addons such as Distillery and Cafe.

## Install Layout

<div class="hl-media-grid">
  <figure class="hl-media-card"><img src="../../images/showcase/install-plugin-overview.webp" alt="Heirloom plugin and addon folder overview"><figcaption>Core and addon jars beside their generated plugin folders.</figcaption></figure>
  <figure class="hl-media-card"><img src="../../images/showcase/install-generated-files.webp" alt="Generated Heirloom files"><figcaption>Generated Heirloom resource files after the first startup.</figcaption></figure>
</div>

## Requirements

- Paper-compatible server for Minecraft 1.21.
- Java version matching the server build you run.
- Heirloom core jar.
- Optional: HeirloomDistillery and HeirloomCafe addon jars.
- Optional visual plugins: Nexo or ItemsAdder.
- Optional protection plugins: WorldGuard, Towny, GriefPrevention, Lands, or similar claim plugins.

## Install Core

1. Stop the server.
2. Put the Heirloom jar in `plugins/`.
3. Start the server once.
4. Confirm `plugins/Heirloom/` was created.
5. Join and run `/hl help`.

## Install Addons

Distillery and Cafe depend on Heirloom. Put addon jars in `plugins/` after core is installed, then restart.

Use:

```text
/hld help
/hlc help
```

## First Files To Review

- `plugins/Heirloom/config.yml`
- `plugins/Heirloom/custom_items.json`
- `plugins/Heirloom/recipes.json`
- `plugins/Heirloom/crops.json`
- `plugins/Heirloom/dietary_properties.json`
- `plugins/Heirloom/seed_acquisition.json`

## Verify The Install

Run `/hl debug test` from an admin account. It checks item registration, recipe matching, crop registration, protection hooks, EcoEnchants detection, and runtime GUI loading.

!!! tip
    If you use a claim plugin, test planting, harvesting, and station use in both allowed and denied regions before opening the server to players.

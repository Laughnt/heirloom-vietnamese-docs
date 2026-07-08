# Updating And Migration Notes

## 2.5 Notes

- Startup banners are standardized and quieter.
- Recipe search is available through `/hl search`.
- Nexo and ItemsAdder visual resolution now share provider-neutral visual IDs.
- Prepared foods should no longer receive hidden hardcoded regeneration or bonus saturation.
- Onion and Allium crop content are bundled.
- Distillery grape crop definitions are restored.

## 2.0 Notes

- Region protection was rewritten around WorldGuard and standard Bukkit events.
- Generic `consume_return` was added.
- EcoEnchants replant and prospector hooks were added.
- Seed packets and world discovery were added.
- Native advancements, mastery, and favourite food systems were expanded.

## Update Checklist

1. Back up `plugins/Heirloom/`.
2. Stop the server.
3. Replace jars.
4. Start and read startup warnings.
5. Run `/hl debug test`.
6. Review custom food balance if you previously worked around hidden effects.

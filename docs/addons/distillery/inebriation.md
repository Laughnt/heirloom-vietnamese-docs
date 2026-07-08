# Inebriation

Distillery tracks drunkenness separately from ordinary food. Drinks can raise a player's level, affect chat through slurring rules, and trigger blackout or wakeup behavior depending on configuration.

Useful commands:

```text
/hld drunk
/hld setdrunk <player> <level>
/hld adddrunk <player> <amount>
/hld wakeup list
```

## Sobering Food

The Heirloom `SOBERING` food property connects back into Distillery. When Distillery is loaded and inebriation is enabled, eating a food with `SOBERING` drains drunkenness by the configured amount, default 15.

Use this for server foods such as strong coffee, greasy meals, or custom hangover cures.

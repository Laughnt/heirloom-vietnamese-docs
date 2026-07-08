# Nexo Integration

Nexo is a soft dependency. Heirloom should load without it.

## Recommended Mapping

Create Nexo items that match Heirloom visual IDs. A common naming convention is:

```text
heirloom_<lowercase_visual_id>
```

Examples:

```text
heirloom_tomato
heirloom_ice_cream_chorus
heirloom_espresso
```

## Testing

Start the server with Nexo installed, run `/hl reload`, then create the item through Heirloom rather than directly through Nexo. That proves the provider path is being used by recipes and commands.

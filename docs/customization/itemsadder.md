# ItemsAdder Integration

ItemsAdder is a soft dependency. Heirloom uses the same logical `visual_id` path for ItemsAdder as it does for Nexo.

## Recommended Mapping

Create ItemsAdder custom stacks for the visual IDs your server wants to replace. Keep IDs stable so recipe actions such as `SET_VISUAL_ITEM` do not need to change.

## Fallback Rule

If ItemsAdder is missing or an item is not mapped, the normal Heirloom item is still created. Test this fallback before launch so players are not blocked by a visual-pack mistake.

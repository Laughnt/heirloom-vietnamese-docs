# Customization

Heirloom content is mostly data-driven. Server owners can customize items, recipes, crops, diet labels, seed acquisition, advancements, and visual mappings.

## Recommended Workflow

1. Make one small JSON change.
2. Validate the file syntax.
3. Run `/hl reload` when the file supports reload.
4. Search the item or recipe in game.
5. Craft it once and inspect the output lore.
6. Only then build the next step of the chain.

This matters because Heirloom recipes can carry metadata forward. A mistake in an intermediate ingredient can affect every later recipe that uses it.

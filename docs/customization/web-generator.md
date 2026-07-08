# Web Generator Workflow

The web generator is useful when you do not want to hand-write recipe JSON.

Use it to draft recipes, then review the exported JSON before putting it on a production server.

Recommended workflow:

1. Build the recipe in the generator.
2. Export JSON.
3. Paste into the correct recipe file.
4. Validate JSON formatting.
5. Run `/hl reload`.
6. Test with `/hl search <recipe>`.
7. Craft the recipe once to confirm actions, inherited properties, return items, and visuals.

Generator link: `https://kernel-person.github.io/heirloom-generator/`

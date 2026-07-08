# Recipe Browser

<figure class="hl-figure">
  <img src="../../images/showcase/recipe-browser.jpg" alt="The recipe browser is the main in-game guide for players.">
  <figcaption>The recipe browser is the main in-game guide for players.</figcaption>
</figure>

## Open It

```text
/hl
/hl recipes
/hl search pizza
```

`/hl` opens the main menu for players. `/hl search <query>` opens filtered results by recipe, station, addon, output, or ingredient.

## Search Examples

<div class="hl-media-grid">
  <figure class="hl-media-card"><img src="../../images/showcase/recipe-search-gui.webp" alt="Recipe search GUI"><figcaption>Recipe search GUI filtered to useful results.</figcaption></figure>
  <figure class="hl-media-card"><img src="../../images/showcase/recipe-search-chat.webp" alt="Recipe search chat output"><figcaption>Chat search output for quick recipe lookup.</figcaption></figure>
</div>

## How To Read It

- Click a recipe to inspect inputs and output.
- Click ingredients to follow recipe chains backward.
- Use item-use pages to answer "what can I cook with this?"
- Addon recipes appear only when their addon is installed and registered.

## If Something Is Missing

- Make sure the addon is installed.
- Run `/hl reload` after JSON changes.
- Check startup logs for recipe validation warnings.
- Use `/hl debug test` for registration diagnostics.

# Recipe Browser

## Open It

```
/hl
/hl recipes
/hl search pizza
```

`/hl` opens the main menu for players. `/hl search <query>` opens filtered results by recipe, station, addon, output, or ingredient.

## Search Examples

## How To Read It

* Click a recipe to inspect inputs and output.
* Click ingredients to follow recipe chains backward.
* Use item-use pages to answer "what can I cook with this?"
* Addon recipes appear only when their addon is installed and registered.

## If Something Is Missing

* Make sure the addon is installed.
* Run `/hl reload` after JSON changes.
* Check startup logs for recipe validation warnings.
* Use `/hl debug test` for registration diagnostics.

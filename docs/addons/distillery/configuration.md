# Distillery Configuration

Important files:

- `plugins/HeirloomDistillery/config.yml`
- `plugins/HeirloomDistillery/ingredients.yml`
- `plugins/HeirloomDistillery/words.yml`
- `plugins/HeirloomDistillery/lang/en.yml`

`/hld reload` reloads supported runtime settings. Restart for jar changes and major data changes.

Development mode can shorten processing loops:

```text
/hld devmode status
/hld devmode on
/hld devmode off
```

## Test After Changes

Run one fruit path and one grain path after config edits. That catches the two most important branches: direct fermentation and Boiling Pot -> fermentation.

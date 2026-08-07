# Heirloom Docs

Public user and admin documentation for the Heirloom Minecraft plugin and the
Heirloom Distillery addon.

## Local Preview

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Open `http://127.0.0.1:8000/`.

## Regenerate Source Reference

The wiki generator reads bundled Core and Cafe JSON plus every release content
pack under `../foodplugin/packs/*/content/`. It rebuilds the item reference,
recipe pages, content-pack pages, navigation, and icon manifest together.

```bash
.venv/bin/python tools/generate_reference_pages.py --use-visual-pack-icons
.venv/bin/python tools/check_content_pack_generation.py
.venv/bin/python tools/check_icon_modes.py
.venv/bin/python tools/check_recipe_slot_badges.py
.venv/bin/mkdocs build --strict
```

Each content pack must use matching `pack` metadata in its item and recipe JSON.
Conflicting metadata stops generation instead of publishing mixed pack data.

## Publish

The included GitHub Actions workflow builds the MkDocs site and publishes it to
GitHub Pages from the `gh-pages` branch.

After the first successful workflow run, enable Pages in the repository
settings:

- Source: Deploy from branch
- Branch: `gh-pages`
- Folder: `/`

Then use the published URL in public plugin listings and any in-game guide link:

```yml
guide-url: "https://kernel-person.github.io/heirloom-docs/"
```

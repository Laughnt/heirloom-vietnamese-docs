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

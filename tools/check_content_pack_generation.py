#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools/generate_reference_pages.py"
PLUGIN_ROOT = Path(os.environ.get("HEIRLOOM_PLUGIN_ROOT", ROOT.parent / "foodplugin")).resolve()
if not PLUGIN_ROOT.exists():
    PLUGIN_ROOT = Path("/Users/rickardmartensson/code/minecraft_plugins/foodplugin/foodplugin")


def load_generator(temp_docs: Path):
    os.environ["HEIRLOOM_DOCS_ROOT"] = str(temp_docs)
    os.environ["HEIRLOOM_PLUGIN_ROOT"] = str(PLUGIN_ROOT)
    module_name = f"heirloom_content_pack_generator_{id(temp_docs)}"
    spec = importlib.util.spec_from_file_location(module_name, GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load generate_reference_pages.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        temp_docs = Path(tmp)
        generator = load_generator(temp_docs)

        packs = {pack["id"]: pack for pack in generator.CONTENT_PACKS}
        asian = packs["heirloom_asian_food"]
        assert asian["name"] == "Heirloom Asian Food Pack"
        assert asian["version"] == "1.0.0"
        assert len(asian["items"]) == 47
        assert len(asian["recipes"]) == 29

        asian_item = next(item for item in generator.ITEMS if item.get("id") == "ASIAN_RICE_FLOUR")
        assert asian_item["_source"] == "Heirloom Asian Food Pack"
        assert asian_item["_pack_id"] == "heirloom_asian_food"

        asian_recipe = next(recipe for recipe in generator.RECIPES if recipe.get("id") == "ASIAN_MISO_SOUP")
        assert asian_recipe["_source"] == "Heirloom Asian Food Pack"
        assert asian_recipe["_pack_id"] == "heirloom_asian_food"

        generator.USE_VISUAL_PACK_ICONS = True
        generator.write_all()

        pack_page = temp_docs / "docs/content-packs/heirloom-asian-food-pack.md"
        assert pack_page.is_file()
        page = pack_page.read_text(encoding="utf-8")
        assert "47 custom items" in page
        assert "29 recipe entries" in page
        assert "ASIAN_MISO_SOUP" in page
        assert "ASIAN_NIGIRI_UNAGI" in page
        assert "Nexo" in page
        assert "ItemsAdder" in page
        assert "CraftEngine" in page
        assert 'src="../../images/items/visual-pack/asian-dumpling-meat.png"' in page
        assert 'src="../images/items/visual-pack/' not in page
        assert 'href="../../reference/items/' in page
        assert 'src="../../images/content-packs/heirloom-asian-food-pack-banner.png"' in page
        assert 'src="../../images/content-packs/heirloom-asian-food-pack-catalog.png"' in page
        assert "source textures are not published" in page

        banner = temp_docs / "docs/images/content-packs/heirloom-asian-food-pack-banner.png"
        assert banner.is_file()
        catalog = temp_docs / "docs/images/content-packs/heirloom-asian-food-pack-catalog.png"
        assert catalog.is_file()

        source_preview = PLUGIN_ROOT / "packs/Heirloom-Asian-Food-Pack-v1.0.0/textures/asian_dumpling_meat.png"
        public_preview = temp_docs / "docs/images/items/visual-pack/asian-dumpling-meat.png"
        width, height, pixels = generator.read_png_rgba(public_preview.read_bytes())
        assert (width, height) == (63, 63)
        assert all(alpha == 255 for _red, _green, _blue, alpha in pixels)
        assert pixels[0] == (255, 253, 245, 255)
        assert generator.ICON_MANIFEST["ASIAN_DUMPLING_MEAT"]["render_style"] == "protected_preview_63_front_relief"
        assert public_preview.read_bytes() != source_preview.read_bytes()

        recipes = (temp_docs / "docs/recipes/default-recipes.md").read_text(encoding="utf-8")
        items = (temp_docs / "docs/reference/items.md").read_text(encoding="utf-8")
        nav = (temp_docs / "mkdocs.yml").read_text(encoding="utf-8")
        assert "ASIAN_MISO_SOUP" in recipes
        assert "Heirloom Asian Food Pack" in recipes
        assert "ASIAN_RICE_FLOUR" in items
        assert "Content Packs:" in nav
        assert "Heirloom Asian Food Pack: content-packs/heirloom-asian-food-pack.md" in nav

        source_images = temp_docs / "docs/images/sources"
        for filename in ("core.png", "cafe.png", "heirloom-asian-food-pack.png"):
            assert (source_images / filename).is_file()

        frying_pan = (temp_docs / "docs/recipes/station-frying-pan.md").read_text(encoding="utf-8")
        assert 'src="../../images/sources/core.png"' in frying_pan
        assert 'src="../../images/sources/heirloom-asian-food-pack.png"' in frying_pan
        assert 'title="Core"' in frying_pan
        assert 'title="Heirloom Asian Food Pack"' in frying_pan
        assert 'src="../../images/sources/heirloom-asian-food-pack.png"' in recipes

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

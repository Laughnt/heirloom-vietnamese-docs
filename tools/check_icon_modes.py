#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

GENERATOR = Path(__file__).with_name("generate_reference_pages.py")
DOCS_ROOT = GENERATOR.parents[1]
PLUGIN_ROOT = DOCS_ROOT.parent / "foodplugin"


def load_generator(temp_docs: Path):
    os.environ["HEIRLOOM_DOCS_ROOT"] = str(temp_docs)
    os.environ["HEIRLOOM_PLUGIN_ROOT"] = str(PLUGIN_ROOT)
    module_name = f"heirloom_generator_under_test_{id(temp_docs)}"
    spec = importlib.util.spec_from_file_location(module_name, GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load generate_reference_pages.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def seed_cached_icon(temp_docs: Path, item_id: str) -> None:
    source = DOCS_ROOT / "docs/images/items/heirloom" / f"{item_id.lower()}.png"
    target = temp_docs / "docs/images/items/heirloom" / f"{item_id.lower()}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def manifest_for_mode(use_visual_pack_icons: bool, item_id: str = "TOMATO") -> tuple[dict, Path]:
    with tempfile.TemporaryDirectory() as tmp:
        temp_docs = Path(tmp)
        cached = DOCS_ROOT / "docs/images/items/heirloom" / f"{item_id.lower().replace('_', '-')}.png"
        if cached.exists():
            seed_cached_icon(temp_docs, item_id.lower().replace("_", "-"))
        generator = load_generator(temp_docs)
        generator.ensure_icon_assets(fetch_icons=False, use_visual_pack_icons=use_visual_pack_icons)
        manifest_path = temp_docs / "docs/images/items/icon-manifest.json"
        entry = json.loads(manifest_path.read_text(encoding="utf-8"))["items"][item_id]
        preview = temp_docs / "docs" / entry["path"]
        preview_bytes = preview.read_bytes() if preview.exists() else b""
        copied_preview = Path(tmp) / "captured-preview.png"
        copied_preview.write_bytes(preview_bytes)
        if preview_bytes:
            width, height, pixels = generator.read_png_rgba(preview_bytes)
            entry["_dimensions"] = [width, height]
            entry["_corner"] = list(pixels[0])
        return entry, copied_preview


def tiny_skin_png(generator) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        skin = Path(tmp) / "skin.png"
        pixels = [(255, 0, 0, 255)] * 64 * 64
        generator.write_png_rgba(skin, 64, 64, pixels)
        return skin.read_bytes()


def stale_player_head_source_refreshes_when_texture_changes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        temp_docs = Path(tmp)
        seed_cached_icon(temp_docs, "fried-chicken")
        manifest_path = temp_docs / "docs/images/items/icon-manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps({
            "minecraft_asset_version": "",
            "items": {
                "FRIED_CHICKEN": {
                    "path": "images/items/heirloom/fried-chicken.png",
                    "source_kind": "player_head_texture",
                    "source_url": "http://textures.minecraft.net/texture/old-fried-chicken",
                    "render_style": "player_head_isometric_v2_80",
                    "status": "ok",
                }
            },
            "recipe_variants": {},
        }), encoding="utf-8")

        generator = load_generator(temp_docs)
        calls = []
        skin = tiny_skin_png(generator)

        def fake_fetch(url: str) -> bytes:
            calls.append(url)
            return skin

        generator.fetch_binary = fake_fetch
        new_texture = "http://textures.minecraft.net/texture/new-fried-chicken"
        generator.ensure_custom_icon({
            "id": "FRIED_CHICKEN",
            "base_material": "PLAYER_HEAD",
            "texture": new_texture,
        }, fetch_icons=True, use_visual_pack_icons=False)

        assert calls == [new_texture], calls
        assert generator.ICON_MANIFEST["FRIED_CHICKEN"]["source_url"] == new_texture


def removed_visual_packs_do_not_leave_public_preview_files() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        temp_docs = Path(tmp)
        stale = temp_docs / "docs/images/items/visual-pack/latte.png"
        stale.parent.mkdir(parents=True, exist_ok=True)
        stale.write_bytes(b"old debug preview")
        generator = load_generator(temp_docs)
        generator.ensure_icon_assets(fetch_icons=False, use_visual_pack_icons=True)
        assert not stale.exists()


def main() -> int:
    assert not (PLUGIN_ROOT / "packs/Heirloom-Cafe-Visual-Pack-v1.0.0").exists()
    assert not (PLUGIN_ROOT / "packs/Heirloom-Cafe-Visual-Pack-v1.0.0.zip").exists()
    default_entry, _ = manifest_for_mode(False)
    tomato_entry, _ = manifest_for_mode(True, "TOMATO")
    corn_entry, _ = manifest_for_mode(True, "CORN")
    asian_entry, _ = manifest_for_mode(True, "ASIAN_MISO_SOUP")

    assert default_entry["source_kind"] != "visual_pack", default_entry
    assert default_entry["path"].startswith("images/items/heirloom/"), default_entry
    assert tomato_entry["source_kind"] != "visual_pack", tomato_entry
    assert corn_entry["source_kind"] != "visual_pack", corn_entry
    assert asian_entry["source_kind"] == "visual_pack", asian_entry
    assert asian_entry["path"].startswith("images/items/visual-pack/"), asian_entry
    assert asian_entry["_dimensions"] == [63, 63], asian_entry
    assert asian_entry["_corner"] == [255, 253, 245, 255], asian_entry
    stale_player_head_source_refreshes_when_texture_changes()
    removed_visual_packs_do_not_leave_public_preview_files()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

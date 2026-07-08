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


def manifest_for_mode(use_visual_pack_icons: bool) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        temp_docs = Path(tmp)
        seed_cached_icon(temp_docs, "tomato")
        generator = load_generator(temp_docs)
        generator.ensure_icon_assets(fetch_icons=False, use_visual_pack_icons=use_visual_pack_icons)
        manifest_path = temp_docs / "docs/images/items/icon-manifest.json"
        return json.loads(manifest_path.read_text(encoding="utf-8"))["items"]["TOMATO"]


def main() -> int:
    default_entry = manifest_for_mode(False)
    visual_entry = manifest_for_mode(True)

    assert default_entry["source_kind"] != "visual_pack", default_entry
    assert default_entry["path"].startswith("images/items/heirloom/"), default_entry
    assert visual_entry["source_kind"] == "visual_pack", visual_entry
    assert visual_entry["path"].startswith("images/items/visual-pack/"), visual_entry
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

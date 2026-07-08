from __future__ import annotations

import argparse
import html
import io
import json
import os
import re
import shutil
import subprocess
import struct
import sys
import urllib.error
import urllib.request
import zipfile
import zlib
from collections import defaultdict
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
if SCRIPT_PATH.parent.name == "tools":
    DEFAULT_DOCS_ROOT = SCRIPT_PATH.parents[1]
else:
    DEFAULT_DOCS_ROOT = Path("/Users/rickardmartensson/code/minecraft_plugins/foodplugin/heirloom-docs")

DOCS_ROOT = Path(os.environ.get("HEIRLOOM_DOCS_ROOT", DEFAULT_DOCS_ROOT)).resolve()
PLUGIN_ROOT = Path(os.environ.get("HEIRLOOM_PLUGIN_ROOT", DOCS_ROOT.parent / "foodplugin")).resolve()
if not PLUGIN_ROOT.exists():
    PLUGIN_ROOT = Path("/Users/rickardmartensson/code/minecraft_plugins/foodplugin/foodplugin")
FETCH_ICONS = False
USE_VISUAL_PACK_ICONS = False
ICON_MANIFEST: dict[str, dict[str, str]] = {}
MISSING_ICON_ROWS: list[tuple[str, str, str]] = []
MINECRAFT_ASSET_INDEX: dict[str, dict] | None = None
MINECRAFT_CLIENT_JAR: zipfile.ZipFile | None = None
MINECRAFT_ASSET_VERSION: str | None = None


def load_existing_icon_manifest() -> dict:
    manifest_path = DOCS_ROOT / "docs/images/items/icon-manifest.json"
    if not manifest_path.exists():
        return {}
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


EXISTING_ICON_MANIFEST = load_existing_icon_manifest()


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def slug(value: str) -> str:
    value = value.strip().lower().replace("_", "-")
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "entry"


def md_escape(value) -> str:
    if value is None:
        return ""
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ").strip()


def title_from_id(value: str) -> str:
    return value.replace("_", " ").title()


def station_key(station: str | None) -> str:
    if not station:
        return "Unknown"
    normalized = station.replace("_", " ").strip().lower()
    aliases = {
        "oven": "Oven",
        "boiling pot": "Boiling Pot",
        "mixing bowl": "Mixing Bowl",
        "cutting board": "Cutting Board",
        "frying pan": "Frying Pan",
        "frying station": "Frying Pan",
        "barista machine": "Barista Machine",
        "stomping tub": "Stomping Tub",
        "fermentation barrel": "Fermentation Barrel",
        "distillation stand": "Distillation Stand",
    }
    return aliases.get(normalized, station.replace("_", " ").title())


def load_items():
    specs = [
        ("Core", PLUGIN_ROOT / "heirloom-core/src/main/resources/custom_items.json"),
        ("World", PLUGIN_ROOT / "heirloom-core/src/main/resources/custom_items-world.json"),
        ("Festive", PLUGIN_ROOT / "heirloom-core/src/main/resources/custom_items-festive.json"),
        ("Cafe", PLUGIN_ROOT / "heirloom-cafe/src/main/resources/custom_items-cafe.json"),
    ]
    items = []
    for source, path in specs:
        if not path.exists():
            continue
        for item in read_json(path).get("custom_items", []):
            row = dict(item)
            row["_source"] = source
            row["_addon"] = row.get("addon") or ("cafe" if source == "Cafe" else "core")
            items.append(row)
    return items


def load_recipes():
    specs = [
        ("Core", PLUGIN_ROOT / "heirloom-core/src/main/resources/recipes.json"),
        ("World", PLUGIN_ROOT / "heirloom-core/src/main/resources/recipes-world.json"),
        ("Festive", PLUGIN_ROOT / "heirloom-core/src/main/resources/recipes-festive.json"),
        ("Cafe", PLUGIN_ROOT / "heirloom-cafe/src/main/resources/recipes-cafe.json"),
    ]
    recipes = []
    for source, path in specs:
        if not path.exists():
            continue
        for recipe_index, recipe in enumerate(read_json(path).get("recipes", [])):
            row = dict(recipe)
            row["_source"] = source
            row["_addon"] = row.get("addon") or ("cafe" if source == "Cafe" else "core")
            row["_station"] = station_key(row.get("station") or row.get("stationName"))
            row["_sequence"] = len(recipes)
            row["_source_index"] = recipe_index
            recipes.append(row)
    return recipes


def load_crops():
    specs = [
        ("Core", PLUGIN_ROOT / "heirloom-core/src/main/resources/crops.json"),
        ("Distillery", PLUGIN_ROOT / "heirloom-core/src/main/resources/crops-distillery.json"),
        ("Cafe", PLUGIN_ROOT / "heirloom-cafe/src/main/resources/crops-cafe.json"),
    ]
    crops = []
    for source, path in specs:
        if not path.exists():
            continue
        data = read_json(path)
        for crop in data.get("crops", []):
            row = dict(crop)
            row["_source"] = source
            row["_addon"] = row.get("addon") or ("cafe" if source == "Cafe" else "core")
            crops.append(row)
    return crops


ITEMS = load_items()
RECIPES = load_recipes()
CROPS = load_crops()
DIET = read_json(PLUGIN_ROOT / "heirloom-core/src/main/resources/dietary_properties.json")
SEEDS = read_json(PLUGIN_ROOT / "heirloom-core/src/main/resources/seed_acquisition.json")
ENCHANTS = read_json(PLUGIN_ROOT / "heirloom-core/src/main/resources/enchantment_integrations.json")

ITEM_BY_ID = {item["id"].upper(): item for item in ITEMS if "id" in item}
RECIPE_BY_ID: dict[str, dict] = {}
RECIPE_ID_COUNTS = defaultdict(int)
for recipe in RECIPES:
    rid = str(recipe.get("id", "")).upper()
    if not rid:
        continue
    RECIPE_BY_ID.setdefault(rid, recipe)
    RECIPE_ID_COUNTS[rid] += 1
    suffix = "" if RECIPE_ID_COUNTS[rid] == 1 else f"-{RECIPE_ID_COUNTS[rid]}"
    recipe["_anchor"] = f"recipe-{slug(rid)}{suffix}"

RECIPES_BY_OUTPUT = defaultdict(list)
for recipe in RECIPES:
    output = str(recipe.get("output", "")).upper()
    if output:
        RECIPES_BY_OUTPUT[output].append(recipe)
    for weighted in recipe.get("weighted_outputs", []) or []:
        output = str(weighted.get("output", "")).upper()
        if output:
            RECIPES_BY_OUTPUT[output].append(recipe)


def collect_vanilla_item_ids() -> set[str]:
    ids: set[str] = set()
    for item in ITEMS:
        base = str(item.get("base_material", "")).upper()
        if base and base != "PLAYER_HEAD":
            ids.add(base)
    for recipe in RECIPES:
        for slot in recipe.get("ingredients", []) or []:
            for option in slot.get("options", []) or []:
                if "item" in option:
                    ids.add(str(option["item"]).upper())
    return {iid for iid in ids if iid and iid not in ITEM_BY_ID}


VANILLA_ITEM_IDS = collect_vanilla_item_ids()


def load_local_visual_pack_icons() -> dict[str, Path]:
    icons: dict[str, Path] = {}
    packs_root = PLUGIN_ROOT / "packs"
    if not packs_root.exists():
        return icons
    for png in packs_root.glob("*/shared/assets/heirloom/textures/item/*.png"):
        icons[png.stem.upper()] = png
    return icons


LOCAL_VISUAL_PACK_ICONS = load_local_visual_pack_icons()


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PLAYER_HEAD_RENDER_STYLE = "player_head_isometric_v2_80"
MINECRAFT_VERSION_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
MINECRAFT_RESOURCE_BASE = "https://resources.download.minecraft.net"
MINECRAFT_ASSET_VERSION_ENV = "HEIRLOOM_MINECRAFT_ASSET_VERSION"


MARKETING_IMAGE_ASSETS = {
    "station-oven": {"source": "station+oven.png", "target": "images/stations/oven", "max_width": 1400},
    "station-boiling-pot": {"source": "station boiling pot.png", "target": "images/stations/boiling-pot", "max_width": 1400},
    "station-mixing-bowl": {"source": "station+mixing+bowl.png", "target": "images/stations/mixing-bowl", "max_width": 1400},
    "station-cutting-board": {"source": "station+cuttingboard.png", "target": "images/stations/cutting-board", "max_width": 1400},
    "station-frying-pan": {"source": "station+frying+table.png", "target": "images/stations/frying-pan", "max_width": 1400},
    "station-barista-machine": {"source": "station-baristamachine.png", "target": "images/stations/barista-machine", "max_width": 1400},
    "crop-lettuce": {"source": "plant+lettuce.png", "target": "images/gardening/lettuce", "max_width": 1400},
    "crop-onion": {"source": "plant+onion.png", "target": "images/gardening/onion", "max_width": 1400},
    "crop-corn": {"source": "plant+cornfield.png", "target": "images/gardening/corn", "max_width": 1400},
    "crop-tomato": {"source": "plant+tomato.png", "target": "images/gardening/tomato", "max_width": 1400},
    "crop-rice": {"source": "plant+ricefield.png", "target": "images/gardening/rice", "max_width": 1400},
    "recipe-search-chat": {"source": "hl+search+chat.png", "target": "images/showcase/recipe-search-chat", "max_width": 1200},
    "recipe-search-gui": {"source": "hl+search+gui.png", "target": "images/showcase/recipe-search-gui", "max_width": 1200},
    "install-plugin-overview": {"source": "installation+pic1.png", "target": "images/showcase/install-plugin-overview", "max_width": 1200},
    "install-generated-files": {"source": "installation+pic+better.png", "target": "images/showcase/install-generated-files", "max_width": 1200},
    "first-meal-build-station": {"source": "getstarted-place-furnace-iron.png", "target": "images/showcase/first-meal-build-station", "max_width": 1400},
    "first-meal-place-egg": {"source": "getstarted-place-egg.png", "target": "images/showcase/first-meal-place-egg", "max_width": 1400},
    "first-meal-cooking-progress": {"source": "getstarted-egg-frying.png", "target": "images/showcase/first-meal-cooking-progress", "max_width": 1400},
    "first-meal-finished": {"source": "getstarted+egg+finished.png", "target": "images/showcase/first-meal-finished", "max_width": 1400},
    "first-meal-wrong-furnace": {"source": "getstarted-cant-use-regular-furnace-better.png", "target": "images/showcase/first-meal-wrong-furnace", "max_width": 1200},
    "food-quality-tooltip": {"source": "quality.png", "target": "images/showcase/food-quality-tooltip", "max_width": 900},
}


def should_update_asset(source: Path, target: Path) -> bool:
    if not target.exists() or target.stat().st_size == 0:
        return True
    return source.stat().st_mtime > target.stat().st_mtime


def convert_marketing_asset(source: Path, target_base: Path, max_width: int) -> None:
    webp_target = target_base.with_suffix(".webp")
    webp_target.parent.mkdir(parents=True, exist_ok=True)
    cwebp = shutil.which("cwebp")
    if cwebp and should_update_asset(source, webp_target):
        cmd = [cwebp, "-quiet", "-q", "82"]
        dimensions = png_dimensions(source)
        if dimensions and dimensions[0] > max_width:
            cmd += ["-resize", str(max_width), "0"]
        cmd += [str(source), "-o", str(webp_target)]
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        if result.returncode == 0 and webp_target.exists() and webp_target.stat().st_size > 0:
            return

    png_target = target_base.with_suffix(".png")
    if not should_update_asset(source, png_target):
        return
    sips = shutil.which("sips")
    dimensions = png_dimensions(source)
    if sips and dimensions and dimensions[0] > max_width:
        result = subprocess.run(
            [sips, "-Z", str(max_width), str(source), "--out", str(png_target)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode == 0 and png_target.exists() and png_target.stat().st_size > 0:
            return
    shutil.copy2(source, png_target)


def sync_marketing_images() -> None:
    source_root = PLUGIN_ROOT / "marketing/wikiimgs"
    if not source_root.exists():
        return
    for config in MARKETING_IMAGE_ASSETS.values():
        source = source_root / config["source"]
        if not source.exists():
            continue
        target_base = DOCS_ROOT / "docs" / config["target"]
        convert_marketing_asset(source, target_base, int(config.get("max_width", 1400)))


def marketing_asset_rel(key: str) -> str | None:
    config = MARKETING_IMAGE_ASSETS.get(key)
    if not config:
        return None
    for ext in (".webp", ".png"):
        rel = f"{config['target']}{ext}"
        if (DOCS_ROOT / "docs" / rel).exists():
            return rel
    return None


def marketing_asset_src(key: str, prefix: str) -> str | None:
    rel = marketing_asset_rel(key)
    if not rel:
        return None
    return f"{prefix}{rel}"


def attr(value) -> str:
    return html.escape(str(value), quote=True)


def read_png_rgba(data: bytes) -> tuple[int, int, list[tuple[int, int, int, int]]]:
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("not a png")
    pos = len(PNG_SIGNATURE)
    width = height = color_type = bit_depth = None
    palette: list[tuple[int, int, int]] = []
    transparency: list[int] = []
    idat = bytearray()
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type, _compression, _filter, _interlace = struct.unpack(">IIBBBBB", chunk)
        elif chunk_type == b"PLTE":
            palette = [tuple(chunk[i:i + 3]) for i in range(0, len(chunk), 3)]
        elif chunk_type == b"tRNS":
            transparency = list(chunk)
        elif chunk_type == b"IDAT":
            idat.extend(chunk)
        elif chunk_type == b"IEND":
            break
    if width is None or height is None or color_type is None:
        raise ValueError("unsupported png")
    if color_type == 3:
        if bit_depth not in (1, 2, 4, 8):
            raise ValueError("unsupported indexed png bit depth")
        channels = 1
        stride = (width * bit_depth + 7) // 8
        filter_bpp = 1
    else:
        if bit_depth != 8:
            raise ValueError("unsupported png bit depth")
        channels_by_type = {0: 1, 2: 3, 4: 2, 6: 4}
        channels = channels_by_type.get(color_type)
        if channels is None:
            raise ValueError("unsupported png color type")
        stride = width * channels
        filter_bpp = channels
    raw = zlib.decompress(bytes(idat))
    rows: list[bytearray] = []
    offset = 0
    prev = bytearray(stride)
    for _y in range(height):
        filter_type = raw[offset]
        scan = bytearray(raw[offset + 1:offset + 1 + stride])
        offset += 1 + stride
        for i, value in enumerate(scan):
            left = scan[i - filter_bpp] if i >= filter_bpp else 0
            up = prev[i]
            up_left = prev[i - filter_bpp] if i >= filter_bpp else 0
            if filter_type == 1:
                scan[i] = (value + left) & 255
            elif filter_type == 2:
                scan[i] = (value + up) & 255
            elif filter_type == 3:
                scan[i] = (value + ((left + up) // 2)) & 255
            elif filter_type == 4:
                p = left + up - up_left
                pa = abs(p - left)
                pb = abs(p - up)
                pc = abs(p - up_left)
                predictor = left if pa <= pb and pa <= pc else up if pb <= pc else up_left
                scan[i] = (value + predictor) & 255
            elif filter_type != 0:
                raise ValueError("unsupported png filter")
        rows.append(scan)
        prev = scan
    pixels: list[tuple[int, int, int, int]] = []
    for row in rows:
        for x in range(width):
            if color_type == 3:
                if bit_depth == 8:
                    index = row[x]
                else:
                    bit_index = x * bit_depth
                    packed = row[bit_index // 8]
                    shift = 8 - bit_depth - (bit_index % 8)
                    index = (packed >> shift) & ((1 << bit_depth) - 1)
                r, g, b = palette[index] if index < len(palette) else (0, 0, 0)
                a = transparency[index] if index < len(transparency) else 255
                pixels.append((r, g, b, a))
                continue
            i = x * channels
            if color_type == 6:
                pixels.append((row[i], row[i + 1], row[i + 2], row[i + 3]))
            elif color_type == 2:
                pixels.append((row[i], row[i + 1], row[i + 2], 255))
            elif color_type == 4:
                pixels.append((row[i], row[i], row[i], row[i + 1]))
            else:
                pixels.append((row[i], row[i], row[i], 255))
    return width, height, pixels


def write_png_rgba(path: Path, width: int, height: int, pixels: list[tuple[int, int, int, int]]) -> None:
    def chunk(kind: bytes, payload: bytes) -> bytes:
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
    rows = bytearray()
    for y in range(height):
        rows.append(0)
        for r, g, b, a in pixels[y * width:(y + 1) * width]:
            rows.extend([r, g, b, a])
    data = PNG_SIGNATURE
    data += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    data += chunk(b"IDAT", zlib.compress(bytes(rows), 9))
    data += chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def png_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        width, height, _pixels = read_png_rgba(path.read_bytes())
        return width, height
    except Exception:
        return None


def blend_pixel(base: tuple[int, int, int, int], overlay: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    if overlay[3] <= 0:
        return base
    if overlay[3] >= 255:
        return overlay
    alpha = overlay[3] / 255
    inv = 1 - alpha
    out_a = overlay[3] + base[3] * inv
    if out_a <= 0:
        return (0, 0, 0, 0)
    return (
        int((overlay[0] * alpha + base[0] * inv)),
        int((overlay[1] * alpha + base[1] * inv)),
        int((overlay[2] * alpha + base[2] * inv)),
        int(min(255, out_a)),
    )


def shade_pixel(pixel: tuple[int, int, int, int], factor: float) -> tuple[int, int, int, int]:
    if pixel[3] <= 0:
        return pixel
    return (
        max(0, min(255, int(pixel[0] * factor))),
        max(0, min(255, int(pixel[1] * factor))),
        max(0, min(255, int(pixel[2] * factor))),
        pixel[3],
    )


def extract_skin_face(width: int, height: int, pixels: list[tuple[int, int, int, int]], x0: int, y0: int, size: int) -> list[tuple[int, int, int, int]]:
    face: list[tuple[int, int, int, int]] = []
    for y in range(size):
        for x in range(size):
            px = x0 + x
            py = y0 + y
            if 0 <= px < width and 0 <= py < height:
                face.append(pixels[py * width + px])
            else:
                face.append((0, 0, 0, 0))
    return face


def merge_face_overlay(base: list[tuple[int, int, int, int]], overlay: list[tuple[int, int, int, int]]) -> list[tuple[int, int, int, int]]:
    return [blend_pixel(base_pixel, overlay_pixel) for base_pixel, overlay_pixel in zip(base, overlay)]


def draw_rgba_pixel(canvas: list[tuple[int, int, int, int]], width: int, height: int, x: int, y: int, color: tuple[int, int, int, int]) -> None:
    if color[3] <= 0 or not (0 <= x < width and 0 <= y < height):
        return
    idx = y * width + x
    canvas[idx] = blend_pixel(canvas[idx], color)


def point_in_polygon(px: float, py: float, polygon: list[tuple[float, float]]) -> bool:
    inside = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        intersects = (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / ((yj - yi) or 1e-9) + xi
        if intersects:
            inside = not inside
        j = i
    return inside


def fill_polygon(canvas: list[tuple[int, int, int, int]], width: int, height: int, polygon: list[tuple[float, float]], color: tuple[int, int, int, int]) -> None:
    min_x = max(0, int(min(x for x, _y in polygon)) - 1)
    max_x = min(width - 1, int(max(x for x, _y in polygon)) + 1)
    min_y = max(0, int(min(y for _x, y in polygon)) - 1)
    max_y = min(height - 1, int(max(y for _x, y in polygon)) + 1)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if point_in_polygon(x + 0.5, y + 0.5, polygon):
                draw_rgba_pixel(canvas, width, height, x, y, color)


def interp_quad(tl: tuple[float, float], tr: tuple[float, float], br: tuple[float, float], bl: tuple[float, float], u: float, v: float) -> tuple[float, float]:
    return (
        (1 - u) * (1 - v) * tl[0] + u * (1 - v) * tr[0] + u * v * br[0] + (1 - u) * v * bl[0],
        (1 - u) * (1 - v) * tl[1] + u * (1 - v) * tr[1] + u * v * br[1] + (1 - u) * v * bl[1],
    )


def draw_textured_quad(
    canvas: list[tuple[int, int, int, int]],
    width: int,
    height: int,
    face: list[tuple[int, int, int, int]],
    face_size: int,
    corners: tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]],
    shade: float,
) -> None:
    tl, tr, br, bl = corners
    for y in range(face_size):
        for x in range(face_size):
            color = shade_pixel(face[y * face_size + x], shade)
            if color[3] <= 0:
                continue
            u0, v0 = x / face_size, y / face_size
            u1, v1 = (x + 1) / face_size, (y + 1) / face_size
            polygon = [
                interp_quad(tl, tr, br, bl, u0, v0),
                interp_quad(tl, tr, br, bl, u1, v0),
                interp_quad(tl, tr, br, bl, u1, v1),
                interp_quad(tl, tr, br, bl, u0, v1),
            ]
            fill_polygon(canvas, width, height, polygon, color)


def fallback_square_face(width: int, height: int, pixels: list[tuple[int, int, int, int]], size: int = 8) -> list[tuple[int, int, int, int]]:
    face_size = min(width, height)
    face_x = max((width - face_size) // 2, 0)
    face_y = max((height - face_size) // 2, 0)
    face: list[tuple[int, int, int, int]] = []
    for y in range(size):
        sy = face_y + y * face_size // size
        for x in range(size):
            sx = face_x + x * face_size // size
            face.append(pixels[sy * width + sx])
    return face


def render_isometric_head_icon(data: bytes, size: int = 80) -> tuple[int, int, list[tuple[int, int, int, int]]]:
    width, height, pixels = read_png_rgba(data)
    unit = 8 if width >= 64 and height >= 16 else min(8, width, height)
    if width >= 64 and height >= 16:
        front = extract_skin_face(width, height, pixels, unit, unit, unit)
        top = extract_skin_face(width, height, pixels, unit, 0, unit)
        side = extract_skin_face(width, height, pixels, unit * 2, unit, unit)
        if width >= unit * 7 and height >= unit * 2:
            front = merge_face_overlay(front, extract_skin_face(width, height, pixels, unit * 5, unit, unit))
            top = merge_face_overlay(top, extract_skin_face(width, height, pixels, unit * 5, 0, unit))
            side = merge_face_overlay(side, extract_skin_face(width, height, pixels, unit * 6, unit, unit))
    else:
        front = fallback_square_face(width, height, pixels, unit)
        top = front
        side = front
    canvas = [(0, 0, 0, 0)] * (size * size)
    scale = size / 40
    def p(x: float, y: float) -> tuple[float, float]:
        return (x * scale, y * scale)
    # Front-facing cube with visible top and right side; source renders large enough for 48px wiki slots.
    top_quad = (p(7, 13), p(27, 13), p(32, 8), p(12, 8))
    side_quad = (p(27, 13), p(32, 8), p(32, 28), p(27, 33))
    front_quad = (p(7, 13), p(27, 13), p(27, 33), p(7, 33))
    draw_textured_quad(canvas, size, size, top, unit, top_quad, 1.08)
    draw_textured_quad(canvas, size, size, side, unit, side_quad, 0.78)
    draw_textured_quad(canvas, size, size, front, unit, front_quad, 1.0)
    return size, size, canvas


def write_system_icon(path: Path, fill: tuple[int, int, int, int], accent: tuple[int, int, int, int]) -> None:
    size = 32
    pixels: list[tuple[int, int, int, int]] = []
    for y in range(size):
        for x in range(size):
            border = x in (0, size - 1) or y in (0, size - 1)
            diagonal = abs(x - y) <= 1 or abs((size - 1 - x) - y) <= 1
            pixels.append(accent if border or diagonal else fill)
    write_png_rgba(path, size, size, pixels)


def fetch_binary(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "Heirloom-Wiki-Icon-Generator/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def fetch_json(url: str) -> dict:
    return json.loads(fetch_binary(url).decode("utf-8"))


def existing_manifest_entry(item_id: str) -> dict:
    return (EXISTING_ICON_MANIFEST.get("items") or {}).get(item_id.upper(), {})


def resolve_minecraft_asset_index() -> tuple[str | None, dict[str, dict]]:
    global MINECRAFT_ASSET_INDEX, MINECRAFT_ASSET_VERSION
    if MINECRAFT_ASSET_INDEX is not None:
        return MINECRAFT_ASSET_VERSION, MINECRAFT_ASSET_INDEX
    version_override = os.environ.get(MINECRAFT_ASSET_VERSION_ENV)
    manifest = fetch_json(MINECRAFT_VERSION_MANIFEST_URL)
    version_id = version_override or manifest.get("latest", {}).get("release")
    version_url = None
    for version in manifest.get("versions", []):
        if version.get("id") == version_id:
            version_url = version.get("url")
            break
    if not version_url:
        raise RuntimeError(f"Minecraft asset version not found: {version_id}")
    version_data = fetch_json(version_url)
    asset_url = version_data.get("assetIndex", {}).get("url")
    if not asset_url:
        raise RuntimeError(f"Minecraft asset index missing for {version_id}")
    asset_index = fetch_json(asset_url).get("objects", {})
    MINECRAFT_ASSET_INDEX = asset_index
    MINECRAFT_ASSET_VERSION = version_id
    return MINECRAFT_ASSET_VERSION, MINECRAFT_ASSET_INDEX


def minecraft_asset_candidates(item_id: str) -> list[str]:
    name = item_id.lower()
    aliases = {
        "water_bottle": ["item/potion.png"],
        "knowledge_book": ["item/knowledge_book.png"],
        "leaf_litter": ["item/leaf_litter.png", "block/leaf_litter.png"],
        "lilac": ["block/lilac_top.png"],
        "peony": ["block/peony_top.png"],
        "pumpkin": ["block/pumpkin_side.png"],
        "rose_bush": ["block/rose_bush_top.png"],
        "sunflower": ["block/sunflower_front.png"],
    }
    paths: list[str] = []
    for alias in aliases.get(name, []):
        paths.append(f"minecraft/textures/{alias}")
    paths.extend([
        f"minecraft/textures/item/{name}.png",
        f"minecraft/textures/block/{name}.png",
    ])
    unique: list[str] = []
    for candidate in paths:
        if candidate not in unique:
            unique.append(candidate)
    return unique


def fetch_minecraft_asset(asset_path: str, asset_index: dict[str, dict]) -> bytes | None:
    entry = asset_index.get(asset_path)
    if not entry:
        return None
    digest = entry.get("hash")
    if not digest:
        return None
    return fetch_binary(f"{MINECRAFT_RESOURCE_BASE}/{digest[:2]}/{digest}")


def resolve_minecraft_client_jar() -> tuple[str | None, zipfile.ZipFile]:
    global MINECRAFT_CLIENT_JAR, MINECRAFT_ASSET_VERSION
    if MINECRAFT_CLIENT_JAR is not None:
        return MINECRAFT_ASSET_VERSION, MINECRAFT_CLIENT_JAR
    version_override = os.environ.get(MINECRAFT_ASSET_VERSION_ENV)
    manifest = fetch_json(MINECRAFT_VERSION_MANIFEST_URL)
    version_id = version_override or manifest.get("latest", {}).get("release")
    version_url = None
    for version in manifest.get("versions", []):
        if version.get("id") == version_id:
            version_url = version.get("url")
            break
    if not version_url:
        raise RuntimeError(f"Minecraft client version not found: {version_id}")
    version_data = fetch_json(version_url)
    client_url = version_data.get("downloads", {}).get("client", {}).get("url")
    if not client_url:
        raise RuntimeError(f"Minecraft client jar missing for {version_id}")
    MINECRAFT_CLIENT_JAR = zipfile.ZipFile(io.BytesIO(fetch_binary(client_url)))
    MINECRAFT_ASSET_VERSION = version_id
    return MINECRAFT_ASSET_VERSION, MINECRAFT_CLIENT_JAR


def fetch_minecraft_texture_from_client(asset_path: str, client_jar: zipfile.ZipFile) -> bytes | None:
    jar_path = f"assets/{asset_path}"
    try:
        return client_jar.read(jar_path)
    except KeyError:
        return None


def record_missing(kind: str, item_id: str, reason: str) -> None:
    normalized = item_id.upper() if kind != "tag" else item_id
    if any(existing_kind == kind and existing_id == normalized for existing_kind, existing_id, _reason in MISSING_ICON_ROWS):
        return
    MISSING_ICON_ROWS.append((kind, normalized, reason))


def texture_hash(texture_url: str) -> str:
    return texture_url.rstrip("/").split("/")[-1]


def icon_rel_for_custom(item_id: str) -> str:
    return f"images/items/heirloom/{slug(item_id)}.png"


def icon_rel_for_vanilla(item_id: str) -> str:
    return f"images/items/minecraft/{slug(item_id)}.png"


def icon_rel_for_visual_pack(item_id: str) -> str:
    return f"images/items/visual-pack/{slug(item_id)}.png"


def ensure_custom_icon(item: dict, fetch_icons: bool, use_visual_pack_icons: bool = False) -> None:
    item_id = str(item.get("id", "")).upper()
    if not item_id:
        return
    texture = item.get("texture")
    base = str(item.get("base_material", "")).upper()
    previous = existing_manifest_entry(item_id)
    local_pack_icon = LOCAL_VISUAL_PACK_ICONS.get(item_id)
    if use_visual_pack_icons and local_pack_icon and local_pack_icon.exists():
        rel = icon_rel_for_visual_pack(item_id)
        target = DOCS_ROOT / "docs" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != local_pack_icon.read_bytes():
            shutil.copyfile(local_pack_icon, target)
        ICON_MANIFEST[item_id] = {
            "path": rel,
            "source": f"visual_pack:{local_pack_icon.relative_to(PLUGIN_ROOT)}",
            "source_kind": "visual_pack",
            "source_url": "",
            "render_style": "texture_2d",
            "minecraft_asset_version": "",
            "status": "ok",
        }
        return
    rel = icon_rel_for_custom(item_id)
    target = DOCS_ROOT / "docs" / rel
    if texture:
        should_refresh = fetch_icons and previous.get("render_style") != PLAYER_HEAD_RENDER_STYLE
        if fetch_icons and (should_refresh or not target.exists()):
            try:
                w, h, pixels = render_isometric_head_icon(fetch_binary(texture))
                write_png_rgba(target, w, h, pixels)
            except Exception:  # noqa: BLE001 - generator should keep building docs
                if not target.exists():
                    record_missing("custom", item_id, "remote player-head fetch unavailable; add local icon")
        if target.exists():
            dimensions = png_dimensions(target)
            ICON_MANIFEST[item_id] = {
                "path": rel,
                "source": "player_head",
                "source_kind": "player_head_texture",
                "source_url": texture,
                "render_style": PLAYER_HEAD_RENDER_STYLE if dimensions == (80, 80) else previous.get("render_style", "cached_player_head"),
                "minecraft_asset_version": "",
                "status": "ok",
            }
            return
    if base and base != "PLAYER_HEAD":
        ensure_vanilla_icon(base, fetch_icons)
        base_entry = ICON_MANIFEST.get(base)
        if base_entry and base_entry.get("status") == "ok":
            ICON_MANIFEST[item_id] = {
                "path": base_entry["path"],
                "source": f"base_material:{base}",
                "source_kind": "base_material",
                "source_url": "",
                "render_style": base_entry.get("render_style", "minecraft_texture"),
                "minecraft_asset_version": base_entry.get("minecraft_asset_version", ""),
                "status": "ok",
            }
            return
    record_missing("custom", item_id, "no cached custom icon")
    ICON_MANIFEST[item_id] = {
        "path": "images/items/system/missing.png",
        "source": "player_head" if texture else f"base:{base}" if base else "missing",
        "source_kind": "missing",
        "source_url": texture or "",
        "render_style": "missing",
        "minecraft_asset_version": "",
        "status": "missing",
    }


def ensure_vanilla_icon(item_id: str, fetch_icons: bool) -> None:
    upper = item_id.upper()
    rel = icon_rel_for_vanilla(upper)
    target = DOCS_ROOT / "docs" / rel
    previous = existing_manifest_entry(upper)
    if target.exists():
        ICON_MANIFEST[upper] = {
            "path": rel,
            "source": previous.get("source", "minecraft_cache"),
            "source_kind": previous.get("source_kind", "minecraft_cache"),
            "source_url": previous.get("source_url", ""),
            "render_style": "minecraft_texture",
            "minecraft_asset_version": previous.get("minecraft_asset_version", "cached"),
            "status": "ok",
        }
        return
    if fetch_icons:
        try:
            version_id, client_jar = resolve_minecraft_client_jar()
            for asset_path in minecraft_asset_candidates(upper):
                data = fetch_minecraft_texture_from_client(asset_path, client_jar)
                if not data:
                    continue
                read_png_rgba(data)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                ICON_MANIFEST[upper] = {
                    "path": rel,
                    "source": f"minecraft_client:{asset_path}",
                    "source_kind": "minecraft_client",
                    "source_url": asset_path,
                    "render_style": "minecraft_texture",
                    "minecraft_asset_version": version_id or "",
                    "status": "ok",
                }
                return
        except Exception:
            record_missing("minecraft", upper, "minecraft client texture fetch unavailable")
    record_missing("minecraft", upper, "no cached vanilla icon")
    ICON_MANIFEST[upper] = {
        "path": "images/items/system/missing.png",
        "source": "minecraft",
        "source_kind": "missing",
        "source_url": "",
        "render_style": "missing",
        "minecraft_asset_version": MINECRAFT_ASSET_VERSION or previous.get("minecraft_asset_version", ""),
        "status": "missing",
    }


def ensure_icon_assets(fetch_icons: bool, use_visual_pack_icons: bool = False) -> None:
    ICON_MANIFEST.clear()
    MISSING_ICON_ROWS.clear()
    items_root = DOCS_ROOT / "docs/images/items"
    (items_root / "heirloom").mkdir(parents=True, exist_ok=True)
    (items_root / "minecraft").mkdir(parents=True, exist_ok=True)
    (items_root / "visual-pack").mkdir(parents=True, exist_ok=True)
    (items_root / "system").mkdir(parents=True, exist_ok=True)
    write_system_icon(items_root / "system/missing.png", (245, 242, 235, 255), (198, 93, 59, 255))
    write_system_icon(items_root / "system/tag.png", (250, 248, 245, 255), (85, 107, 47, 255))
    (DOCS_ROOT / "docs/images/stations").mkdir(parents=True, exist_ok=True)
    for iid in sorted(VANILLA_ITEM_IDS):
        ensure_vanilla_icon(iid, fetch_icons)
    for item in sorted(ITEMS, key=lambda i: str(i.get("id", ""))):
        ensure_custom_icon(item, fetch_icons, use_visual_pack_icons)
    manifest = {
        "generated_by": "tools/generate_reference_pages.py",
        "fetch_icons": fetch_icons,
        "use_visual_pack_icons": use_visual_pack_icons,
        "minecraft_asset_version": MINECRAFT_ASSET_VERSION or EXISTING_ICON_MANIFEST.get("minecraft_asset_version", ""),
        "items": ICON_MANIFEST,
        "missing": [
            {"kind": kind, "id": item_id, "reason": reason}
            for kind, item_id, reason in sorted(MISSING_ICON_ROWS)
        ],
    }
    (items_root / "icon-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def item_markdown_href(item_id: str, prefix: str = "../reference/") -> str | None:
    upper = item_id.upper()
    if upper in ITEM_BY_ID:
        return f"{prefix}items.md#{item_anchor(upper)}"
    if upper in VANILLA_ITEM_IDS or upper in ICON_MANIFEST:
        return f"{prefix}vanilla-items.md#{vanilla_item_anchor(upper)}"
    return None


def item_html_href(item_id: str, prefix: str = "../reference/") -> str | None:
    upper = item_id.upper()
    if upper in ITEM_BY_ID:
        return f"{prefix}items/#{item_anchor(upper)}"
    if upper in VANILLA_ITEM_IDS or upper in ICON_MANIFEST:
        return f"{prefix}vanilla-items/#{vanilla_item_anchor(upper)}"
    return None


def icon_img(item_id: str, image_prefix: str = "../", title: str | None = None, css_class: str = "") -> str:
    upper = item_id.upper()
    entry = ICON_MANIFEST.get(upper, {"path": "images/items/system/missing.png", "status": "missing"})
    classes = "hl-item-icon"
    if entry.get("status") != "ok":
        classes += " hl-icon-missing"
    if css_class:
        classes += f" {css_class}"
    label = title or upper
    return f'<img class="{classes}" src="{image_prefix}{entry["path"]}" alt="{attr(upper)}" title="{attr(label)}">'


def icon_link(item_id: str, href_prefix: str = "../reference/", image_prefix: str = "../", title: str | None = None) -> str:
    href = item_html_href(item_id, href_prefix)
    image_html = icon_img(item_id, image_prefix, title)
    if href:
        return f'<a class="hl-icon-link" href="{attr(href)}">{image_html}</a>'
    return image_html


def tag_icon(tag: str, image_prefix: str = "../", title: str | None = None) -> str:
    label = title or f"tag: {tag}"
    src = f"{image_prefix}images/items/system/tag.png"
    record_missing("tag", tag, "tag ingredients use a generic icon")
    return f'<img class="hl-item-icon hl-icon-missing" src="{src}" alt="{attr(label)}" title="{attr(label)}">'


def vanilla_item_anchor(item_id: str) -> str:
    return f"vanilla-item-{slug(item_id)}"


def recipe_anchor(recipe: dict | str) -> str:
    if isinstance(recipe, dict):
        return recipe.get("_anchor") or f"recipe-{slug(str(recipe.get('id', 'recipe')))}"
    upper = str(recipe).upper()
    found = RECIPE_BY_ID.get(upper)
    if found:
        return recipe_anchor(found)
    return f"recipe-{slug(upper)}"


def item_anchor(item_id: str) -> str:
    return f"item-{slug(item_id)}"


def crop_anchor(crop_id: str) -> str:
    return f"crop-{slug(crop_id)}"


def item_link(item_id: str, prefix: str = "../reference/") -> str:
    upper = item_id.upper()
    href = item_markdown_href(upper, prefix)
    if href:
        return f"[`{upper}`]({href})"
    return f"`{upper}`"


def recipe_link(recipe: dict | str, prefix: str = "../recipes/") -> str:
    if isinstance(recipe, dict):
        upper = str(recipe.get("id", "")).upper()
        return f"[`{upper}`]({prefix}default-recipes.md#{recipe_anchor(recipe)})"
    upper = str(recipe).upper()
    return f"[`{upper}`]({prefix}default-recipes.md#{recipe_anchor(upper)})"


def recipe_output_markdown_href(output_id: str, recipe_prefix: str = "../recipes/", reference_prefix: str = "../reference/") -> str | None:
    upper = output_id.upper()
    if upper in RECIPES_BY_OUTPUT:
        first = RECIPES_BY_OUTPUT[upper][0]
        return f"{recipe_prefix}default-recipes.md#{recipe_anchor(first)}"
    return item_markdown_href(upper, reference_prefix)


def recipe_output_html_href(output_id: str, recipe_prefix: str = "../recipes/", reference_prefix: str = "../reference/", recipe: dict | None = None) -> str | None:
    upper = output_id.upper()
    if upper in RECIPES_BY_OUTPUT:
        target_recipe = recipe or RECIPES_BY_OUTPUT[upper][0]
        anchor = recipe_anchor(target_recipe)
        if recipe_prefix == "#":
            return f"#{anchor}"
        return f"{recipe_prefix}default-recipes/#{anchor}"
    return item_html_href(upper, reference_prefix)


def recipe_output_link(output_id: str, prefix: str = "../recipes/") -> str:
    upper = output_id.upper()
    href = recipe_output_markdown_href(upper, prefix, "../reference/")
    if href:
        return f"[`{upper}`]({href})"
    return f"`{upper}`"


def output_icon_cell(output_id: str, recipe_prefix: str = "../recipes/", reference_prefix: str = "../reference/", image_prefix: str = "../", recipe: dict | None = None) -> str:
    upper = output_id.upper()
    href = recipe_output_html_href(upper, recipe_prefix, reference_prefix, recipe)
    visual = icon_img(upper, image_prefix, title=upper, css_class="hl-output-icon")
    body = f'{visual}<span class="hl-output-name">{upper}</span>'
    if href:
        return f'<a class="hl-output-item" href="{attr(href)}">{body}</a>'
    return f'<span class="hl-output-item">{body}</span>'


def format_options(options: list[dict], prefix: str = "../reference/") -> str:
    parts = []
    for option in options:
        if "custom_item" in option:
            parts.append(item_link(option["custom_item"], prefix))
        elif "item" in option:
            parts.append(item_link(option["item"], prefix))
        elif "tag" in option:
            parts.append(f"`#{option['tag']}`")
    return " or ".join(parts) if parts else "any"


def slot_quantity_bounds(slot: dict) -> tuple[int, int]:
    max_count = int(slot.get("max", 1) or 1)
    min_value = slot.get("min")
    slot_type = str(slot.get("type", "REQUIRED")).lower()
    if min_value is None:
        min_count = 0 if slot_type == "optional" else 1
    else:
        min_count = int(min_value)
    return min_count, max_count


def slot_quantity_text(slot: dict) -> str:
    min_count, max_count = slot_quantity_bounds(slot)
    if min_count == max_count:
        return str(max_count)
    return f"{min_count}-{max_count}"


def slot_count_badge(slot: dict) -> str:
    min_count, max_count = slot_quantity_bounds(slot)
    if min_count == max_count:
        if max_count == 1:
            return ""
        label = str(max_count)
    else:
        label = f"{min_count}-{max_count}"
    return f'<span class="hl-slot-count">{attr(label)}</span>'


def ingredient_summary(recipe: dict, prefix: str = "../reference/") -> str:
    bits = []
    for slot in recipe.get("ingredients", []) or []:
        label = slot.get("type", "REQUIRED").lower()
        count = slot_quantity_text(slot)
        bits.append(f"{label}: {count} x {format_options(slot.get('options', []), prefix)}")
    return "<br>".join(bits) if bits else "none"


def slot_count_label(slot: dict) -> str:
    return f"{str(slot.get('type', 'REQUIRED')).lower()}: {slot_quantity_text(slot)}"


def option_label(option: dict) -> str:
    if "custom_item" in option:
        return str(option["custom_item"]).upper()
    if "item" in option:
        return str(option["item"]).upper()
    if "tag" in option:
        return f"#{option['tag']}"
    return "ANY"


def option_icon(option: dict, href_prefix: str, image_prefix: str, title: str, linked: bool = True) -> str:
    if "custom_item" in option:
        item_id = str(option["custom_item"]).upper()
        return icon_link(item_id, href_prefix, image_prefix, title) if linked else icon_img(item_id, image_prefix, title)
    if "item" in option:
        item_id = str(option["item"]).upper()
        return icon_link(item_id, href_prefix, image_prefix, title) if linked else icon_img(item_id, image_prefix, title)
    if "tag" in option:
        return tag_icon(str(option["tag"]), image_prefix, title)
    return tag_icon("any", image_prefix, title)


def ingredient_icon_strip(recipe: dict, href_prefix: str = "../reference/", image_prefix: str = "../") -> str:
    slots: list[str] = []
    for index, slot in enumerate(recipe.get("ingredients", []) or [], start=1):
        options = list(slot.get("options", []) or [])
        if not options:
            continue
        slot_type = str(slot.get("type", "REQUIRED")).lower()
        slot_class = "hl-slot-optional" if slot_type == "optional" else "hl-slot-required"
        quantity = slot_quantity_text(slot)
        labels = [option_label(option) for option in options]
        readable_type = "Optional" if slot_type == "optional" else "Required"
        title = f"{readable_type} slot {index}: {quantity}; " + " or ".join(labels)
        count_badge = slot_count_badge(slot)
        if len(options) == 1:
            icon = option_icon(options[0], href_prefix, image_prefix, title, linked=True)
            slots.append(
                f'<span class="hl-ingredient-slot {slot_class}" title="{attr(title)}">'
                f'<span class="hl-slot-box">{icon}{count_badge}</span>'
                f'</span>'
            )
            continue
        alternatives = []
        for option_index, option in enumerate(options):
            if option_index:
                alternatives.append('<span class="hl-choice-separator">or</span>')
            alternatives.append(option_icon(option, href_prefix, image_prefix, f"{option_label(option)} - {title}", linked=True))
        slots.append(
            f'<span class="hl-ingredient-slot {slot_class}" title="{attr(title)}">'
            f'<span class="hl-slot-box"><span class="hl-slot-choice-icons" aria-label="{attr(title)}">'
            f'{"".join(alternatives)}</span>{count_badge}</span></span>'
        )
    if not slots:
        return '<span class="hl-small">none</span>'
    return '<span class="hl-recipe-slots">' + "".join(slots) + "</span>"


def output_visual_row(recipe: dict, recipe_prefix: str = "../recipes/", reference_prefix: str = "../reference/", image_prefix: str = "../") -> str:
    return output_icon_cell(str(recipe.get("output", "")), recipe_prefix, reference_prefix, image_prefix, recipe)

def actions_summary(recipe: dict) -> str:
    actions = list(recipe.get("actions", []) or [])
    for rule in recipe.get("rules", []) or []:
        actions.extend(rule.get("actions", []) or [])
    if recipe.get("weighted_outputs"):
        weighted = ", ".join(
            f"{entry.get('output')} ({entry.get('weight')})"
            for entry in recipe.get("weighted_outputs", [])
        )
        actions.append({"type": "weighted_outputs", "value": weighted})
    useful = []
    for action in actions:
        t = action.get("type", "")
        value = action.get("value", "")
        key = action.get("key")
        if key:
            useful.append(f"`{t}` `{key}` = `{value}`")
        elif value:
            useful.append(f"`{t}` = `{value}`")
        else:
            useful.append(f"`{t}`")
    return "<br>".join(useful) if useful else "-"


def table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(md_escape(cell) for cell in row) + " |")
    return "\n".join(out)


PAGES: dict[str, str] = {}


def add(path: str, content: str):
    PAGES[path] = content.strip() + "\n"


def page(title: str, body: str) -> str:
    return f"# {title}\n\n{body.strip()}\n"


def image(src: str, caption: str, alt: str | None = None) -> str:
    alt = alt or caption
    return (
        f'<figure class="hl-figure">\n'
        f'  <img src="{src}" alt="{alt}">\n'
        f'  <figcaption>{caption}</figcaption>\n'
        f'</figure>'
    )




STATION_CAPTURE_TARGETS = {
    "Oven": "docs/images/stations/oven.webp",
    "Boiling Pot": "docs/images/stations/boiling-pot.webp",
    "Mixing Bowl": "docs/images/stations/mixing-bowl.webp",
    "Cutting Board": "docs/images/stations/cutting-board.webp",
    "Frying Pan": "docs/images/stations/frying-pan.webp",
    "Barista Machine": "docs/images/stations/barista-machine.webp",
}


def docs_image_exists(src: str | None) -> bool:
    if not src or re.match(r"^[a-z]+:", src):
        return False
    normalized = src
    while normalized.startswith("../"):
        normalized = normalized[3:]
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return (DOCS_ROOT / "docs" / normalized).exists()


def image_if(src: str | None, caption: str, alt: str | None = None) -> str:
    if not docs_image_exists(src):
        return ""
    return image(src or "", caption, alt)


def media_card(src: str, caption: str, alt: str | None = None, href: str | None = None) -> str:
    alt = attr(alt or caption)
    caption_attr = attr(caption)
    image_html = f'<img src="{attr(src)}" alt="{alt}">'
    if href:
        image_html = f'<a class="hl-media-link" href="{attr(href)}">{image_html}</a>'
    return f'<figure class="hl-media-card">{image_html}<figcaption>{caption_attr}</figcaption></figure>'


def media_card_if(src: str | None, caption: str, alt: str | None = None, href: str | None = None) -> str:
    if not docs_image_exists(src):
        return ""
    return media_card(src or "", caption, alt, href)


def media_grid(cards: list[str]) -> str:
    visible = [card for card in cards if card]
    if not visible:
        return ""
    return '<div class="hl-media-grid">\n' + "\n".join(f"  {card}" for card in visible) + "\n</div>"


def station_media(title: str) -> str:
    candidates: dict[str, list[tuple[str | None, str]]] = {
        "Oven": [(marketing_asset_src("station-oven", "../../"), "Oven station built from a stone pressure plate on a smoker.")],
        "Boiling Pot": [
            (marketing_asset_src("station-boiling-pot", "../../"), "Boiling Pot station built over a campfire."),
            ("../../images/showcase/jam.gif", "Boiling Pot cooking flow with visible station effects."),
        ],
        "Mixing Bowl": [(marketing_asset_src("station-mixing-bowl", "../../"), "Mixing Bowl station built with a flower pot on stripped wood.")],
        "Cutting Board": [
            (marketing_asset_src("station-cutting-board", "../../"), "Cutting Board station built with a wooden pressure plate on stripped wood."),
            ("../../images/showcase/wheat.gif", "Cutting Board chopping flow with visible prep interaction."),
        ],
        "Frying Pan": [
            (marketing_asset_src("station-frying-pan", "../../"), "Frying Pan station built from a heavy weighted pressure plate on a furnace."),
            ("../../images/stations/frying-pan.gif", "Frying Pan cooking flow on a furnace station."),
        ],
        "Barista Machine": [(marketing_asset_src("station-barista-machine", "../../"), "Cafe Barista Machine built from an iron trapdoor over quartz stairs.")],
    }
    figures = [image(src, caption) for src, caption in candidates.get(title, []) if docs_image_exists(src)]
    return "\n\n".join(figures)


def crop_media(crop_id: str) -> str:
    crop_assets = {
        "LETTUCE": ("crop-lettuce", "Lettuce crop planted as a short ground crop."),
        "ONION": ("crop-onion", "Onion crop planted as an allium-style ground crop."),
        "CORN": ("crop-corn", "Corn field showing tall crop visuals."),
        "TOMATO": ("crop-tomato", "Tomato crop growing as a vine."),
        "RICE": ("crop-rice", "Rice crop planted in water above soil."),
    }
    entry = crop_assets.get(crop_id)
    if not entry:
        return ""
    src = marketing_asset_src(entry[0], "../../")
    return image_if(src, entry[1])


def crop_media_cards(prefix: str, href_prefix: str) -> list[str]:
    crops = [
        ("LETTUCE", "crop-lettuce", "Lettuce", "Short ground crop."),
        ("ONION", "crop-onion", "Onion", "Allium-style ground crop."),
        ("CORN", "crop-corn", "Corn", "Tall crop with vertical room."),
        ("TOMATO", "crop-tomato", "Tomato", "Wall vine crop."),
        ("RICE", "crop-rice", "Rice", "Aquatic crop planted in water."),
    ]
    cards = []
    for crop_id, asset_key, label, caption in crops:
        src = marketing_asset_src(asset_key, prefix)
        href = f"{href_prefix}{slug(crop_id)}/"
        cards.append(media_card_if(src, f"{label}: {caption}", label, href))
    return cards


def gardening_crop_grid() -> str:
    grid = media_grid(crop_media_cards("../", ""))
    if not grid:
        return ""
    return "## Crop Gallery\n\n" + grid


def recipe_search_media() -> str:
    grid = media_grid([
        media_card_if(marketing_asset_src("recipe-search-gui", "../../"), "Recipe search GUI filtered to useful results.", "Recipe search GUI"),
        media_card_if(marketing_asset_src("recipe-search-chat", "../../"), "Chat search output for quick recipe lookup.", "Recipe search chat output"),
    ])
    if not grid:
        return ""
    return "## Search Examples\n\n" + grid


def first_farm_media() -> str:
    grid = media_grid(crop_media_cards("../../", "../../gardening/"))
    if not grid:
        return ""
    return "## Crop Examples\n\n" + grid


def installation_media() -> str:
    grid = media_grid([
        media_card_if(marketing_asset_src("install-plugin-overview", "../../"), "Core and addon jars beside their generated plugin folders.", "Heirloom plugin and addon folder overview"),
        media_card_if(marketing_asset_src("install-generated-files", "../../"), "Generated Heirloom resource files after the first startup.", "Generated Heirloom files"),
    ])
    if not grid:
        return ""
    return "## Install Layout\n\n" + grid


def first_meal_media() -> str:
    flow = media_grid([
        media_card_if(marketing_asset_src("first-meal-build-station", "../../"), "Build the Frying Pan from a furnace and heavy weighted pressure plate.", "Frying Pan setup"),
        media_card_if(marketing_asset_src("first-meal-place-egg", "../../"), "Right-click with an egg to place it as a visible ingredient.", "Egg placed on the Frying Pan"),
        media_card_if(marketing_asset_src("first-meal-cooking-progress", "../../"), "Start cooking with an empty hand and watch the progress feedback.", "Fried Egg cooking progress"),
        media_card_if(marketing_asset_src("first-meal-finished", "../../"), "Collect the finished Fried Egg from the station.", "Finished Fried Egg on the station"),
    ])
    warning = media_grid([
        media_card_if(marketing_asset_src("first-meal-wrong-furnace", "../../"), "The vanilla furnace GUI does not cook Heirloom recipes; interact with the physical station instead.", "Vanilla furnace GUI cannot cook Heirloom recipes"),
    ])
    sections = []
    if flow:
        sections.append("## First Meal Visual Flow\n\n" + flow)
    if warning:
        sections.append("## Common Wrong Turn\n\n" + warning)
    return "\n\n".join(sections)


def cooking_basics_media() -> str:
    grid = media_grid([
        media_card_if(marketing_asset_src("first-meal-place-egg", "../../"), "Ingredients are placed into the world as visible station contents.", "Egg displayed on station"),
        media_card_if(marketing_asset_src("first-meal-cooking-progress", "../../"), "Cooking starts from the station interaction, with progress shown in game.", "Station cooking progress"),
        media_card_if(marketing_asset_src("first-meal-wrong-furnace", "../../"), "Opening the vanilla furnace GUI is a sign you are using the wrong interaction path.", "Wrong furnace GUI interaction"),
    ])
    if not grid:
        return ""
    return "## Station Loop Example\n\n" + grid


def quality_media() -> str:
    src = marketing_asset_src("food-quality-tooltip", "../../")
    media = image_if(src, "Quality and dietary data are visible directly in item lore.", "Food quality tooltip")
    if not media:
        return ""
    return "## Quality Tooltip Example\n\n" + media


def gallery_media_sections() -> str:
    sections = []
    overview = media_grid([
        media_card_if("../images/showcase/recipe-browser.jpg", "Recipe browsing and ingredient lookup.", "Recipe browser"),
        media_card_if(marketing_asset_src("recipe-search-gui", "../"), "Recipe search GUI.", "Recipe search GUI", "../getting-started/recipe-browser/"),
        media_card_if(marketing_asset_src("recipe-search-chat", "../"), "Recipe search from chat.", "Recipe search chat", "../getting-started/recipe-browser/"),
        media_card_if(marketing_asset_src("install-plugin-overview", "../"), "Installation folder layout.", "Heirloom install folders", "../getting-started/installation/"),
        media_card_if(marketing_asset_src("first-meal-build-station", "../"), "First meal station setup.", "First meal station setup", "../getting-started/first-meal/"),
        media_card_if(marketing_asset_src("first-meal-cooking-progress", "../"), "First meal cooking progress.", "First meal cooking progress", "../getting-started/first-meal/"),
        media_card_if(marketing_asset_src("first-meal-wrong-furnace", "../"), "Wrong furnace interaction example.", "Furnace GUI warning", "../player-guide/cooking/"),
        media_card_if(marketing_asset_src("food-quality-tooltip", "../"), "Food quality tooltip.", "Food quality tooltip", "../player-guide/quality/"),
        media_card_if("../images/showcase/rice.gif", "Rice growth and display visuals.", "Rice crop"),
        media_card_if("../images/showcase/jam.gif", "Cooking flow and recipe variants.", "Jam cooking"),
        media_card_if("../images/showcase/christmas-placeable.png", "Placeable seasonal food.", "Placeable food"),
        media_card_if("../images/showcase/advancements.png", "Advancement UI.", "Advancements"),
        media_card_if("../images/showcase/cooking-mastery.png", "Cooking mastery UI.", "Cooking mastery"),
    ])
    if overview:
        sections.append("## Gameplay And UI\n\n" + overview)

    station_cards = []
    for title, asset_key, href in [
        ("Oven", "station-oven", "../stations/oven/"),
        ("Boiling Pot", "station-boiling-pot", "../stations/boiling-pot/"),
        ("Mixing Bowl", "station-mixing-bowl", "../stations/mixing-bowl/"),
        ("Cutting Board", "station-cutting-board", "../stations/cutting-board/"),
        ("Frying Pan", "station-frying-pan", "../stations/frying-pan/"),
        ("Barista Machine", "station-barista-machine", "../stations/barista-machine/"),
    ]:
        station_cards.append(media_card_if(marketing_asset_src(asset_key, "../"), f"{title} station.", title, href))
    station_grid = media_grid(station_cards)
    if station_grid:
        sections.append("## Cooking Stations\n\n" + station_grid)

    crop_grid = media_grid(crop_media_cards("../", "../gardening/"))
    if crop_grid:
        sections.append("## Crops\n\n" + crop_grid)

    distillery = media_grid([
        media_card_if("../images/distillery/D_stomp_grain.gif", "Stomping tub.", "Stomping grain"),
        media_card_if("../images/distillery/D_boil_wort.gif", "Boiling grain wort.", "Boiling wort"),
        media_card_if("../images/distillery/D_wine_ferment.gif", "Wine fermentation.", "Wine fermentation"),
        media_card_if("../images/distillery/D_whiskey.gif", "Distillation output.", "Whiskey distillation"),
    ])
    if distillery:
        sections.append("## Distillery Motion\n\n" + distillery)
    return "\n\n".join(sections)


def station_recipe_table(station: str, recipe_prefix: str = "../recipes/", reference_prefix: str = "../reference/", image_prefix: str = "../") -> str:
    rows = []
    for recipe in sorted([r for r in RECIPES if r["_station"] == station], key=lambda r: (r["id"], r.get("_sequence", 0))):
        rows.append([
            recipe_link(recipe),
            output_visual_row(recipe, recipe_prefix, reference_prefix, image_prefix),
            ingredient_icon_strip(recipe, reference_prefix, image_prefix),
            recipe.get("_source", ""),
        ])
    if not rows:
        return "No bundled recipes currently use this station."
    return table(["Recipe", "Output", "Inputs", "Source"], rows)


STATION_GUIDES = {
    "Oven": """
## How Recipes Behave Here

The Oven is the long-form heat station. It is where raw prep becomes shelf-stable or baked food: dough becomes bread, flat dough becomes pizza, wet coffee cherries become roast beans, and some addon chains use it as the first serious processing step.

## Common Chains

- `BAG_OF_FLOUR` -> `DOUGH` -> bread, pizza, pancakes, waffles, doughnuts, and pastry-style recipes.
- Cafe coffee cherries roast through light, medium, and dark beans before they become espresso drinks.
- Recipes with `SET_RETURN_ITEM` can give containers back after the craft, so check the output and your inventory before assuming a bucket or bottle vanished.

## Good First Recipes

Start with bread or baked potato-style recipes before testing pizzas and addon chains. They prove the station structure works without requiring several intermediate ingredients.

## What Can Go Wrong

If a recipe never starts, first confirm the station is the smoker plus stone pressure plate pair. If the station works but a recipe does not match, search the exact output or ingredient with `/hl search <query>`; many baked foods need an intermediate Heirloom item rather than the raw vanilla ingredient.
""",
    "Boiling Pot": """
## How Recipes Behave Here

The Boiling Pot is the liquid and simmering station. It handles soups, rice, pasta, cheese, jam, wet ingredient conversions, and recipes that care about buckets or bottles. It is also where property stacking becomes easy to understand: jam can become an ingredient in later foods while keeping the food properties created from its fruit.

## Common Chains

- Fruit + sugar + bottle -> `JAM`; glow berries, golden apples, and chorus fruit can add food properties to the jam.
- `RICE` + water -> `COOKED_RICE`, which then feeds sushi and fried rice chains.
- Milk bucket -> `CHEESE`, and milk plus vinegar can produce the alternate cheese path.
- Distillery grain wort uses the Boiling Pot before fermentation.

## Good First Recipes

Try `COOKED_RICE`, `CHEESE`, then `JAM`. Those three cover water inputs, bucket returns, bottle returns, and property-carrying ingredients.

## What Can Go Wrong

A bucket can be either a normal Minecraft interaction or a recipe ingredient. If you are testing a recipe, interact normally with the station and avoid vanilla cauldron habits. If the output keeps the wrong flavor or property, inspect the recipe rules: properties come from matching ingredient rules and from inherited input data.
""",
    "Mixing Bowl": """
## How Recipes Behave Here

The Mixing Bowl is for combining, folding, grinding, and cold prep. It often creates neutral intermediates that later become powerful when cooked elsewhere: dough, batter, cream, plant protein, and Cafe grinding steps all live here.

## Common Chains

- Flour and liquids become `DOUGH`, then the Oven or Frying Pan finishes the dish.
- Cafe uses grinding-style recipes for tea leaves, matcha chances, and other drink prep.
- Mixed ingredients can inherit dietary and food-property data from custom inputs, so the bowl is often where a server-owner recipe starts carrying metadata forward.

## Good First Recipes

Use the bowl for dough and cream before testing more advanced recipe chains. These are easier to debug because their ingredients are obvious.

## What Can Go Wrong

If a recipe looks right but does not match, check whether the input wants a custom item such as `BAG_OF_FLOUR` rather than vanilla `WHEAT`. For server owners, this station is a good place to test optional slots because it makes failures easy to see before cooking time is involved.
""",
    "Cutting Board": """
## How Recipes Behave Here

The Cutting Board is prep work: chopping, slicing, mincing, and turning raw ingredients into precise recipe components. It is intentionally not a generic table; many recipes need the prepared form before another station accepts them.

## Common Chains

- `WHEAT` can become flour-style ingredients used by dough and batter chains.
- Meat and plant alternatives can become minced or sliced components for later meals.
- Pasta and similar prep items are made here before being boiled or cooked.

## Good First Recipes

Start with flour or pasta prep. Those recipes teach the difference between vanilla ingredients and Heirloom intermediate items.

## What Can Go Wrong

Use the correct physical station: wooden pressure plate on a stripped block. If a food chain seems blocked, search the output you expected; the missing step is often a Cutting Board ingredient rather than the final station.
""",
    "Frying Pan": """
## How Recipes Behave Here

The Frying Pan is fast heat. It handles eggs, bacon, pancakes, fried rice, and other foods where toppings and optional ingredients change the final item. This station is one of the clearest places to see inherited properties: a special jam used as a pancake topping can carry `CHORUS`, `GOLDEN`, or other properties into the finished pancakes.

## Common Chains

- Eggs and bacon prove the station works with simple vanilla inputs.
- `PANCAKES` accept flour/cornmeal, eggs, milk, and optional toppings such as `JAM`, honey, or chocolate.
- `FRIED_RICE` and similar recipes usually depend on rice being cooked first at the Boiling Pot.

## Good First Recipes

Cook a plain egg, then pancakes, then pancakes with a custom jam. Compare the lore: the topping can change name, quality, return behavior, and inherited food properties.

## What Can Go Wrong

The recipe can be valid but still produce a plain-looking result if the optional ingredient did not match the rule you expected. For example, bundled honey pancakes add honey naming, quality, and bottle return behavior; they do not add `SWEET` unless a recipe or custom ingredient explicitly stores that food property.
""",
    "Barista Machine": """
## How Recipes Behave Here

The Barista Machine is Cafe's drink assembly station. Earlier Cafe steps happen on core stations: cherries roast in the Oven, leaves and powders use prep stations, and the Barista Machine turns those prepared ingredients into drinks.

## Common Chains

- Coffee cherry -> light beans -> medium beans -> dark beans -> espresso -> americano, latte, cappuccino, flat white, mocha, or iced coffee.
- Leaves -> dried or ground tea ingredients -> green tea, black tea, sweet tea, matcha latte, or boba tea.
- Milk bucket and oat milk variants often change names, returns, and dietary behavior.

## Good First Recipes

Pull `ESPRESSO`, then make `AMERICANO`, then a milk drink. That proves the chain, the station, and container returns.

## What Can Go Wrong

The station only registers when Cafe is installed. If the trapdoor and quartz stairs act like normal blocks, confirm the Cafe jar loaded, `/hlc help` works, and Cafe recipes appear in `/hl search cafe`.
""",
}


def station_page(title: str, build: str, use: str, station: str, tips: str) -> str:
    media = station_media(title)
    guide = STATION_GUIDES.get(title, "")
    return page(title, f"""
## Build

{build}

{media}

## Core Loop

{use}

{guide}

## Recipes

{station_recipe_table(station, "../../recipes/", "../../reference/", "../../")}

## Troubleshooting

{tips}

See the full [recipe index](../recipes/default-recipes.md) for ingredient links, processing time, recipe rules, and output actions.
""")


def crop_page(crop_id: str) -> str:
    crop = next((c for c in CROPS if c.get("id") == crop_id), None)
    if not crop:
        return page(title_from_id(crop_id), "This crop is not present in the current bundled data.")
    growth = crop.get("growth", {})
    planting = crop.get("planting", {})
    harvest = crop.get("harvest", {})
    rows = [
        ["Item", item_link(crop.get("item_id", crop_id))],
        ["Plant type", f"`{crop.get('plant_type', '')}`"],
        ["Base growth", f"{growth.get('base_duration_seconds', '?')} seconds"],
        ["Stages", str(growth.get("stages", "?"))],
        ["Permission", f"`{planting.get('permission', 'none')}`"],
        ["Replants", "`yes`" if harvest.get("replant_after_harvest", True) else "`no`"],
    ]
    drops = ", ".join(
        f"`{d.get('item_id')}` {d.get('min', 1)}-{d.get('max', 1)}"
        for d in harvest.get("drops", [])
    ) or "none"
    valid_blocks = ", ".join(f"`{b}`" for b in planting.get("valid_blocks", [])) or "see crop JSON"
    media = crop_media(crop_id)
    return page(title_from_id(crop_id), f"""
{media}

{table(["Field", "Value"], rows)}

## Planting

Valid blocks: {valid_blocks}

Use the crop item on the correct block or face. If the crop has a permission, the player must have that node before planting.

## Harvest

Main drops: {drops}.

If the crop keeps `replant_after_harvest` enabled, right-click harvest resets it to an early stage. Breaking the plant is treated as destruction, not a full harvest.

## Notes For Admins

Edit this crop in `crops.json` or the relevant addon crop file. Growth scale, stage count, valid blocks, sounds, drop chances, quality chance, and permission nodes are all data-driven.
""")
def build_recipe_index() -> str:
    sections = ["# Default Recipe Index", "", "This page is generated from the bundled recipe JSON files. It is meant for lookup; the station pages explain how the systems feel in play.", ""]
    for station in sorted({r["_station"] for r in RECIPES}):
        sections.append(f"## {station}")
        sections.append("")
        for recipe in sorted([r for r in RECIPES if r["_station"] == station], key=lambda r: (r["id"], r.get("_sequence", 0))):
            rid = recipe["id"].upper()
            sections.append(f"### {rid} {{ #{recipe_anchor(recipe)} }}")
            rows = [
                ["Output", output_visual_row(recipe, "#", "../../reference/", "../../")],
                ["Source", recipe.get("_source", "")],
                ["Processing time", f"{recipe.get('processing_time', 0)} ticks"],
                ["Visual inputs", ingredient_icon_strip(recipe, "../../reference/", "../../")],
                ["Ingredients", ingredient_summary(recipe)],
                ["Rules and actions", actions_summary(recipe)],
            ]
            if recipe.get("description"):
                rows.insert(1, ["Description", recipe.get("description", "")])
            sections.append(table(["Field", "Value"], rows))
            sections.append("")
    return "\n".join(sections)


def build_item_reference() -> str:
    sections = ["# Item ID Reference", "", "Source-derived reference for bundled Heirloom custom items. Use these IDs in commands, recipes, visual mappings, and config files.", ""]
    seen_ids: set[str] = set()
    for source in ["Core", "World", "Festive", "Cafe"]:
        group = sorted([i for i in ITEMS if i["_source"] == source and i.get("id")], key=lambda i: i.get("id", ""))
        if not group:
            continue
        sections.append(f"## {source} Items")
        sections.append("")
        rows = []
        for item in group:
            iid = str(item.get("id", "")).upper()
            if not iid or iid in seen_ids:
                continue
            seen_ids.add(iid)
            rows.append([
                icon_img(iid, "../../"),
                f'<span id="{item_anchor(iid)}"></span>`{iid}`',
                item.get("name", title_from_id(iid)),
                item.get("base_material", ""),
                "yes" if item.get("edible") else "no",
                item.get("visual_id", iid),
            ])
        sections.append(table(["Icon", "ID", "Name", "Base", "Edible", "Visual ID"], rows))
        sections.append("")
    return "\n".join(sections)




def build_vanilla_item_reference() -> str:
    sections = ["# Vanilla Ingredient Reference", "", "Source-derived list of vanilla Minecraft items used by bundled Heirloom recipes or as custom item base materials.", ""]
    rows = []
    for item_id in sorted(VANILLA_ITEM_IDS):
        rows.append([
            icon_img(item_id, "../../"),
            f'<span id="{vanilla_item_anchor(item_id)}"></span>`{item_id}`',
            title_from_id(item_id),
            ICON_MANIFEST.get(item_id, {}).get("status", "missing"),
        ])
    sections.append(table(["Icon", "ID", "Name", "Icon status"], rows))
    return "\n".join(sections)


def build_crop_reference() -> str:
    sections = ["# Crop ID Reference", "", "Source-derived reference for bundled crop definitions.", ""]
    rows = []
    for crop in sorted(CROPS, key=lambda c: (c["_source"], c.get("id", ""))):
        cid = crop.get("id", "")
        growth = crop.get("growth", {})
        planting = crop.get("planting", {})
        rows.append([
            f'<span id="{crop_anchor(cid)}"></span>`{cid}`',
            crop.get("_source", ""),
            crop.get("item_id", ""),
            crop.get("plant_type", ""),
            str(growth.get("base_duration_seconds", "")),
            planting.get("permission", ""),
        ])
    sections.append(table(["ID", "Source", "Item", "Type", "Base seconds", "Permission"], rows))
    return "\n".join(sections)


def build_recipe_reference() -> str:
    rows = []
    by_source = defaultdict(int)
    by_station = defaultdict(int)
    for recipe in RECIPES:
        by_source[recipe["_source"]] += 1
        by_station[recipe["_station"]] += 1
    for source, count in sorted(by_source.items()):
        rows.append([source, str(count)])
    station_rows = [[station, str(count)] for station, count in sorted(by_station.items())]
    return page("Recipe Reference", f"""
The full linked recipe index lives at [Default Recipe Index](../recipes/default-recipes.md).

## Recipes By Source

{table(["Source", "Recipes"], rows)}

## Recipes By Station

{table(["Station", "Recipes"], station_rows)}

## Data Files

- `recipes.json`: main core recipes.
- `recipes-world.json`: optional world-food recipes.
- `recipes-festive.json`: seasonal recipes and feast recipes.
- `recipes-cafe.json`: Cafe addon recipes.
""")


def build_visual_reference() -> str:
    rows = []
    for item in sorted([i for i in ITEMS if i.get("visual_id")], key=lambda i: i["id"]):
        rows.append([f"`{item['id']}`", item.get("visual_id", ""), item.get("_source", "")])
    return page("Visual ID Reference", f"""
`visual_id` is the logical name Heirloom asks visual providers to resolve. Nexo and ItemsAdder can both provide the same logical visual without changing recipes.

{table(["Item", "Visual ID", "Source"], rows)}
""")




def missing_icon_section() -> str:
    rows = []
    for kind, item_id, reason in sorted(MISSING_ICON_ROWS):
        rows.append([kind, f"`{item_id}`", reason])
    if not rows:
        return "No missing recipe icons were detected in the last generator run."
    return table(["Kind", "ID", "Reason"], rows)


def basic_pages():
    add("index.md", page("Heirloom Wiki", f"""
{image("images/heirloom-wide-banner.png", "Heirloom is a physical cooking and gardening plugin for Paper servers.")}

Heirloom adds in-world cooking stations, custom crops, food quality, dietary labels, recipe discovery, and addon content without requiring a resource pack. Optional Nexo and ItemsAdder integrations can replace the player-head fallback visuals when a server wants a resource-pack presentation.

## Start Here

- New players: [First Meal](getting-started/first-meal.md), [First Farm](getting-started/first-farm.md), then [Recipe Browser](getting-started/recipe-browser.md).
- Server owners: [Installation](getting-started/installation.md), [Configuration](server-owners/configuration.md), [Permissions](server-owners/permissions.md), and [Diagnostics](server-owners/diagnostics.md).
- Creators: [Custom Foods](customization/custom-foods.md), [Custom Recipes](customization/custom-recipes.md), [Custom Crops](customization/custom-crops.md), and [Visual Integrations](customization/visuals-overview.md).

## What The Wiki Covers

<div class="hl-grid">
  <div class="hl-card"><h3>Players</h3><p>Cooking, farming, recipe search, favourite food, advancements, mastery, and feasts.</p></div>
  <div class="hl-card"><h3>Server Owners</h3><p>Install, configure, protect claims, localize, debug, and update safely.</p></div>
  <div class="hl-card"><h3>Creators</h3><p>Write JSON content, tune food systems, and map visual items for Nexo or ItemsAdder.</p></div>
  <div class="hl-card"><h3>Addons</h3><p>Distillery and Cafe have full pages. Future addons are tracked separately.</p></div>
</div>

## Useful Links

- Web recipe generator: `https://kernel-person.github.io/heirloom-generator/`
- Demo video: `https://youtu.be/t10v5fPzius?si=xZ4-q1KusBYcF8NP`
- Discord: `https://discord.gg/bPeuK6drX3`

## Current Public Addons

- [Distillery](addons/distillery/index.md): wine, beer, spirits, mashables, traits, inebriation, and processing stations.
- [Cafe](addons/cafe/index.md): coffee, tea, barista recipes, coffee cherries, and cafe visual packs.
"""))

    add("gallery.md", page("Gallery", f"""
The gallery collects media that already exists in the docs project. Missing captures are tracked in [Media Needed](media-needed.md).

{gallery_media_sections()}
"""))


    add("roadmap.md", page("Future Addons", """
This wiki documents public, usable gameplay first. The repository also contains early work for future addon modules.

| Addon | Current wiki status | Notes |
| --- | --- | --- |
| Tides | Roadmap only | Fishing addon work exists, but command implementation is not ready for a public guide. |
| Pasture | Roadmap only | Animal husbandry systems are in development. |
| Neighbours | Roadmap only | Quest/social systems are experimental and should not be documented as stable gameplay yet. |

When these modules are ready, they should get the same treatment as Distillery and Cafe: player guide, server owner setup, commands, permissions, config, and media checklist.
"""))

    add("media-needed.md", page("Media Needed", f"""
Capture these in-game images and GIFs before publishing a fully visual version of the wiki. Keep captures clean: default UI scale, readable chat/action bars, no unrelated builds in frame, and one subject per shot.

## Highest Priority

| Page | Needed media | Notes |
| --- | --- | --- |
| Home | Current kitchen overview screenshot | Show all five core stations in one compact kitchen. |
| First Farm | Planting and harvest flow screenshots | Still crop images exist; capture the interaction flow. |
| Favourite Food | Favourite food GUI screenshot | Show current favourite and selection state. |
| Placeable Foods | Feast before/after serving screenshots | Include servings remaining if visible. |
| Cafe | Drink flow screenshot set | Barista Machine still exists; add espresso, latte, and tea flow. |

## Advanced / Server Owner

| Page | Needed media | Notes |
| --- | --- | --- |
| Visual Integrations | Nexo/ItemsAdder comparison | Same item with fallback and custom visual. |
| Diagnostics | `/hl debug test` output | Use a clean successful run. |
| Region Protection | Protected-region denial action bar | Show crop or station interaction blocked. |
| Dietary Properties | Item lore examples | Vegan/Vegetarian/Gluten-Free plus Contains line. |

## Recipe Icon Gaps

These are generated from the latest icon pass. Tag entries use a generic tag icon by design. Missing custom or Minecraft icons should be replaced with local PNGs under `docs/images/items/`.

{missing_icon_section()}

## Distillery

Existing Distillery GIFs are usable. Add still screenshots for the Distillery command menu, Brew Lab, traits browser, and drunk level/status output.
"""))


def getting_started_pages():
    add("getting-started/installation.md", page("Installation", f"""
Heirloom is a Paper plugin for modern Minecraft 1.21 servers. Install the core plugin first, then add optional addons such as Distillery and Cafe.

{installation_media()}

## Requirements

- Paper-compatible server for Minecraft 1.21.
- Java version matching the server build you run.
- Heirloom core jar.
- Optional: HeirloomDistillery and HeirloomCafe addon jars.
- Optional visual plugins: Nexo or ItemsAdder.
- Optional protection plugins: WorldGuard, Towny, GriefPrevention, Lands, or similar claim plugins.

## Install Core

1. Stop the server.
2. Put the Heirloom jar in `plugins/`.
3. Start the server once.
4. Confirm `plugins/Heirloom/` was created.
5. Join and run `/hl help`.

## Install Addons

Distillery and Cafe depend on Heirloom. Put addon jars in `plugins/` after core is installed, then restart.

Use:

```text
/hld help
/hlc help
```

## First Files To Review

- `plugins/Heirloom/config.yml`
- `plugins/Heirloom/custom_items.json`
- `plugins/Heirloom/recipes.json`
- `plugins/Heirloom/crops.json`
- `plugins/Heirloom/dietary_properties.json`
- `plugins/Heirloom/seed_acquisition.json`

## Verify The Install

Run `/hl debug test` from an admin account. It checks item registration, recipe matching, crop registration, protection hooks, EcoEnchants detection, and runtime GUI loading.

!!! tip
    If you use a claim plugin, test planting, harvesting, and station use in both allowed and denied regions before opening the server to players.
"""))

    add("getting-started/first-meal.md", page("First Meal", f"""
This walkthrough makes a simple cooked food and teaches the physical station flow.

{first_meal_media()}

## Goal

Cook Fried Egg on a Frying Pan.

## Build The Frying Pan

Place a `FURNACE`, then place a `HEAVY_WEIGHTED_PRESSURE_PLATE` on top. The plate is the station block players interact with.

## Cook

1. Hold an egg.
2. Right-click the frying pan to add it.
3. Empty your hand.
4. Right-click the station to begin cooking.
5. Wait for the completion effects.
6. Left-click to collect the result, or add more ingredients if the result is part of another recipe chain.

## What To Notice

- The station stores visible ingredients as display entities.
- Some stations need tools for best results, such as chopping tools on the Cutting Board.
- Recipe quality can improve with correct station interaction and Cooking Mastery.

Next: [First Farm](first-farm.md) or [Recipe Browser](recipe-browser.md).
"""))

    add("getting-started/first-farm.md", page("First Farm", f"""
Start with Lettuce because it uses the simplest plant type.

{first_farm_media()}

## Get A Crop Item

Admins can test with:

```text
/hl give LETTUCE
```

Players normally discover seeds through grass drops, seed packets, chest loot, or world generation, depending on server configuration.

## Plant Lettuce

1. Hold `LETTUCE`.
2. Right-click grass, dirt, coarse dirt, podzol, or rooted dirt.
3. Wait for the display to mature.
4. Right-click the mature crop to harvest.

## Try The Other Core Crops

- Lettuce: short ground plant.
- Onion: allium-style ground plant.
- Corn: tall plant.
- Tomato: wall vine.
- Rice: aquatic crop planted in water above soil.

See [Gardening](../gardening/index.md) for conditions, permissions, and drops.
"""))

    add("getting-started/recipe-browser.md", page("Recipe Browser", f"""
{image("../../images/showcase/recipe-browser.jpg", "The recipe browser is the main in-game guide for players.")}

## Open It

```text
/hl
/hl recipes
/hl search pizza
```

`/hl` opens the main menu for players. `/hl search <query>` opens filtered results by recipe, station, addon, output, or ingredient.

{recipe_search_media()}

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
"""))


def player_pages():
    add("player-guide/index.md", page("Player Guide", """
This section explains Heirloom as a game system rather than a config file. Read it when you want to know what a player is expected to do, what the item lore means, and why a recipe result changed.

Start with [Cooking Basics](cooking.md), then use [Recipe Search](recipe-search.md), [Favourite Food](favourite-food.md), [Food Quality](quality.md), and [Farming And Seed Discovery](seed-discovery.md).
"""))
    add("player-guide/cooking.md", page("Cooking Basics", f"""
Heirloom cooking is physical. You build a station in the world, add visible ingredients, process the station, then either collect the result or keep using that result as part of a recipe chain.

{cooking_basics_media()}

## The Station Loop

1. Build the correct station shape.
2. Right-click with ingredients to place them on the station.
3. Empty your hand and right-click to begin processing.
4. Wait for the station effects and progress to finish.
5. Left-click to collect the output, or keep the output in the station flow if the next recipe uses it.

## Chains Are The Point

Many foods are not one-step crafts. Flour can become dough, dough can become bread or pancakes, rice can become cooked rice and then a meal, and jam can become a topping that carries properties into another food. When a recipe says it wants `JAM`, it means the actual item you made, including quality, creator data, consume returns, and food properties.

## What Changes A Result

A finished food can be changed by recipe rules, optional ingredients, inherited properties, quality, and visual actions. That is why two foods with the same output ID can have different names, lore, textures, or effects.

## Container Returns

Some recipes and foods return buckets or bottles. There are two common cases:

- Craft return: the station gives something back when the recipe completes.
- Consume return: eating the food gives something back afterward, such as a bottle from jam.

## Common Failure Cases

- The station shape is wrong, so Heirloom never treats the block as a station.
- The ingredient is the wrong form, such as `WHEAT` instead of `BAG_OF_FLOUR`.
- The recipe belongs to another station or addon.
- An optional ingredient matched the base recipe but not the rule you expected.
- A protection plugin cancelled interaction in the region.

Use `/hl search <ingredient>` when stuck. It is usually faster than guessing the next station.
"""))
    add("player-guide/recipe-search.md", page("Recipe Search", f"""
`/hl search <query>` searches recipes by name, station, addon, ingredient, or output. It is the fastest way to follow a chain backward.

{recipe_search_media()}

Examples:

```text
/hl search pizza
/hl search rice
/hl search oven
/hl search cafe
/hl search jam
```

## How To Use Search Well

Search the ingredient you are holding, not only the food you want. If you have `RICE`, search rice to find cooked rice and later meal paths. If you have `JAM`, search jam to find pancakes, doughnuts, or any server-added recipes that use it.

## Recipe Detail Preview

The in-game recipe detail view simulates the selected inputs. When a selected ingredient has food properties or dietary data, the preview can show the resulting lore before you cook it.
"""))
    add("player-guide/favourite-food.md", page("Favourite Food", """
Favourite food is a personal RPG feature. You choose one custom food, then get extra effects whenever you eat that food ID.

## Command

```text
/hl favourite
```

Aliases:

```text
/hl favorite
/hl fav
```

## What You Get

Eating your favourite food applies:

| Effect | Duration | Strength |
| --- | --- | --- |
| Regeneration | 30 seconds | I |
| Saturation | 15 seconds | II |
| Luck | 60 seconds | I |

These effects are added after normal food-property effects. If your favourite food is also a property-stacked food, both systems apply.

## Why It Matters

A plain favourite is useful. A favourite with inherited properties is stronger. For example, pancakes made with `GOLDEN` and `CHORUS` jam can apply those property effects, then the favourite-food package if pancakes are your selected favourite.

## Social Cooking

Heirloom stores cooked-by data on edible outputs. If somebody else cooked your favourite food, the favourite check can reward the cook with a short regeneration effect. The `AFFINITY` food property also reads cooked-by data and becomes stronger when the food is also your favourite.

## Server Notes For Players

If `/hl favourite` is unavailable, ask staff whether `heirloom.favourite` is granted. The feature is permission-gated so servers can decide whether it is part of default progression.
"""))
    add("player-guide/quality.md", page("Food Quality", f"""
Food quality is stored on custom foods and ingredients. It is not just flavor text: quality is part of progression, advancement tracking, and recipe identity.

## What Changes Quality

- Recipe actions can set a base quality or add to it.
- Ingredient quality can carry into later foods; the crafting code keeps the best input quality when no explicit quality is supplied.
- Crops can store quality and keep it when replanted after harvest.
- Cooking Mastery adds a recipe-specific quality bonus as you repeat the same recipe.

## Reading Quality In Play

Quality appears in item names and lore. If two players make the same recipe but one uses better ingredients or has more mastery, their outputs can differ.

{quality_media()}

## Why It Matters

Quality supports long-term goals: better crops, better repeated cooking, and quality-based advancements. If a recipe feels unrewarding, check whether it is setting quality too low or never inheriting quality from its ingredients.

Server owners can inspect the data side in [Custom Recipes](../customization/custom-recipes.md).
"""))
    add("player-guide/advancements.md", page("Advancements", f"""
{image("../../images/showcase/advancements.png", "Heirloom has native advancement progress.")}

Heirloom tracks food discovery, crop harvesting, recipe progress, collection goals, and quality milestones.

Commands:

```text
/hl advancements
/hl adv
/hl progress
```

## How Progress Is Counted

Eating custom foods records the food ID and quality. Harvesting crops records crop progress. Collection advancements check whether you have eaten or harvested every item in a list, while counter advancements check totals.

Admins can customize bundled advancement data in `advancements.json`.
"""))
    add("player-guide/mastery.md", page("Cooking Mastery", f"""
{image("../../images/showcase/cooking-mastery.png", "Cooking Mastery rewards repeated practice with a recipe.")}

Cooking Mastery tracks how often you cook each recipe. Mastery is recipe-specific: being excellent at pancakes does not automatically make you excellent at sushi.

Command:

```text
/hl mastery
```

## Levels

| Level | Crafts | Quality bonus |
| --- | ---: | ---: |
| Novice | 0 | 0% |
| Apprentice | 5 | +5% |
| Competent | 15 | +10% |
| Skilled | 30 | +15% |
| Expert | 50 | +20% |
| Master | 80 | +30% |

The bonus is added to the recipe quality roll. This makes frequently cooked foods more reliable without making every recipe globally easier.
"""))
    add("player-guide/placeable-foods.md", page("Placeable Foods And Feasts", f"""
{image("../../images/showcase/christmas-placeable.png", "Some foods can be placed and eaten in servings.")}

Some Heirloom foods can be placed and eaten in servings. The placed block stores remaining servings, remaining nutrition, remaining saturation, and food properties in block data so state survives restarts.

## How To Eat

Right-click the placed food with an empty hand. Each bite consumes one serving and applies that serving's share of nutrition, saturation, and any stored food-property effects.

## Feasts

Feast foods track unique participants. When a new guest joins a feast, previous participants receive a small regeneration bonus. This rewards shared meals without giving the same player repeated guest credit.

## Breaking Placed Food

Breaking a placed food removes it and plays food-colored break particles. It does not return the whole food item.
"""))
    add("player-guide/seed-discovery.md", page("Farming And Seed Discovery", """
Players can obtain crop starts in several ways, depending on server settings.

## Discovery Methods

- Grass drops from valid grass or fern blocks.
- Seed packets that open into weighted seed drops.
- Chest loot in villages, dungeons, mineshafts, and temples.
- Natural crop patches in new chunks.
- Admin commands during testing.

## What To Try First

Break grass in a biome that matches the crop you want, explore village/farm-style loot, then use seed packets when you find them. Rice and other special crops may be weighted toward specific biome groups rather than appearing everywhere.

## Seed Packets

Temperate packets focus on lettuce, corn, tomato, onion, and some vanilla crops. Tropical packets focus on rice and warm-climate vanilla seeds.

See [Seed Packets](../gardening/seed-packets.md) for exact data.
"""))


def station_pages():
    add("stations/index.md", page("Cooking Stations", """
Stations are built from normal blocks. Players interact with the station block, while Heirloom validates the supporting structure below or nearby.

| Station | Build | Main Role |
| --- | --- | --- |
| Oven | Stone pressure plate on a smoker | Baking, roasting, drying, long heat chains |
| Boiling Pot | Cauldron or water cauldron over a campfire or soul campfire | Soups, rice, pasta, cheese, jam, wet recipes |
| Mixing Bowl | Flower pot on any stripped block | Dough, creams, mixed prep, grinding-style steps |
| Cutting Board | Wooden pressure plate on any stripped block | Chopping, slicing, mincing, flour and prep items |
| Frying Pan | Heavy weighted pressure plate on a furnace | Eggs, pancakes, fried meals, fast heat |
| Barista Machine | Iron trapdoor above quartz stairs, with Cafe installed | Cafe drink assembly |

## How To Think About Stations

Stations are not skins for one crafting menu. Each station teaches a different kind of recipe: prep stations make intermediate ingredients, heat stations transform them, and addon stations finish specialized chains. If a recipe does not match, search the ingredient and check the station before assuming the item is broken.

Each station page lists practical first recipes, common chains, and its generated recipe table.
"""))
    add("stations/oven.md", station_page(
        "Oven",
        "Build an Oven with a `STONE_PRESSURE_PLATE` on top of a `SMOKER`.",
        "The Oven handles baking, roasting, drying, and some chain steps such as bread, pizza, and coffee roasting.",
        "Oven",
        "If the station does not activate, confirm the plate is directly above a smoker and that the clicked block is the plate.",
    ))
    add("stations/boiling-pot.md", station_page(
        "Boiling Pot",
        "Build a Boiling Pot with a `CAULDRON` or `WATER_CAULDRON` over a `CAMPFIRE` or `SOUL_CAMPFIRE`.",
        "The Boiling Pot handles wet recipes, soups, cheese, rice, pasta, and recipes that return buckets or bottles.",
        "Boiling Pot",
        "Water buckets are recipe ingredients for some recipes. Avoid sneak-right-clicking when you mean to add the bucket as an ingredient, because sneak interaction may allow vanilla cauldron behavior.",
    ))
    add("stations/mixing-bowl.md", station_page(
        "Mixing Bowl",
        "Build a Mixing Bowl with a `FLOWER_POT` on any `STRIPPED_` log, wood, stem, hyphae, or bamboo block.",
        "The Mixing Bowl handles dough, mixing, cold preparation, and Cafe grinding steps.",
        "Mixing Bowl",
        "Use a shovel-style tool for mixing interactions. In survival, use a pickaxe if you intend to break the station cleanly.",
    ))
    add("stations/cutting-board.md", station_page(
        "Cutting Board",
        "Build a Cutting Board with any wooden pressure plate on any `STRIPPED_` block.",
        "The Cutting Board handles prep work such as flour, pasta, minced ingredients, and sliced recipe steps.",
        "Cutting Board",
        "Use sword or axe-style tools for chopping interactions. Non-wood pressure plates are reserved for other stations or ignored.",
    ))
    add("stations/frying-pan.md", station_page(
        "Frying Pan",
        "Build a Frying Pan with a `HEAVY_WEIGHTED_PRESSURE_PLATE` on top of a `FURNACE`.",
        "The Frying Pan handles eggs, bacon, pancakes, fried rice, and other fast heated foods.",
        "Frying Pan",
        "If a recipe does not match, use `/hl search <ingredient>` and confirm every ingredient belongs at this station.",
    ))
    add("stations/barista-machine.md", station_page(
        "Barista Machine",
        "Build a Barista Machine with an `IRON_TRAPDOOR` above `QUARTZ_STAIRS`. The Cafe addon must be installed and registered.",
        "The Barista Machine pulls espresso, tea, cocoa, boba, iced drinks, and milk-based drinks from Cafe ingredients.",
        "Barista Machine",
        "If the station acts like normal blocks, confirm HeirloomCafe loaded and `/hlc help` works.",
    ))


def recipes_pages():
    add("recipes/index.md", page("Recipes", """
Recipes are loaded from JSON and indexed into the in-game browser. Players usually use `/hl recipes` or `/hl search`, while server owners edit JSON files.

## How To Read Recipe Docs

- Station pages explain workflow and list recipes by station.
- [Default Recipe Index](default-recipes.md) is the full linked lookup.
- [Recipe Chains](recipe-chains.md) explains common progression paths.

## Important Concepts

- Required and optional ingredient slots.
- Recipe rules that change names, quality, properties, visuals, or return items.
- Weighted outputs for recipes with chance-based results.
- Addon recipes that appear only when their addon registers.
"""))
    for station, filename in [
        ("Oven", "station-oven.md"),
        ("Boiling Pot", "station-boiling-pot.md"),
        ("Mixing Bowl", "station-mixing-bowl.md"),
        ("Cutting Board", "station-cutting-board.md"),
        ("Frying Pan", "station-frying-pan.md"),
        ("Barista Machine", "station-barista-machine.md"),
    ]:
        add(f"recipes/{filename}", page(f"{station} Recipes", station_recipe_table(station, "../", "../../reference/", "../../")))
    add("recipes/default-recipes.md", build_recipe_index())
    add("recipes/recipe-chains.md", page("Recipe Chains", """
Some Heirloom recipes are deliberately chained. A station result can stay on the station and become an ingredient in the next step.

## Common Chains

- Flour -> dough -> bread, pizza, pasta, pancakes, doughnuts.
- Rice -> cooked rice -> sushi-style recipes.
- Corn -> cornmeal -> taco shell and related recipes.
- Coffee cherry -> light beans -> medium beans -> dark beans -> espresso drinks.
- Green tea leaves -> dried green tea -> chance for matcha powder -> matcha latte.

## How To Explore Chains In Game

Use `/hl search <ingredient>` or click ingredients in the recipe browser. The wiki index links recipe outputs back to the recipe that creates them where possible.
"""))


def gardening_pages():
    add("gardening/index.md", page("Gardening", f"""
{image("../images/showcase/rice.gif", "Heirloom crops use custom display visuals and growth stages.")}

Core crops are Lettuce, Onion, Corn, Tomato, and Rice. Addons can register additional crops, such as Distillery grapes and Cafe coffee cherries.

{gardening_crop_grid()}

## What A Crop Is

A crop is a real block plus a display entity and stored data. The block gives Minecraft something to protect, break, and interact with; the display gives Heirloom its custom visual stages; stored data tracks crop ID, growth state, facing, and optional quality.

## The Growth Loop

1. Obtain a crop item or seed packet.
2. Plant it on a valid block for its plant type.
3. Let the growth timer advance through stages.
4. Right-click the mature crop to harvest.
5. If `replant_after_harvest` is enabled, the crop resets to an early stage instead of disappearing.

## Crop Types At A Glance

- Lettuce is the simplest short ground crop.
- Onion uses allium-style placement.
- Corn is a tall crop and needs vertical room.
- Tomato is a vine and needs a wall face.
- Rice is aquatic and needs water above valid soil.

## Quality And Drops

Harvest settings define normal drops, bonus drops, replanting, sounds, and quality chance. Fortune can improve configured bonus drops, and compatible custom enchantments can add effective Fortune or force replanting.

## Acquisition

Survival access comes from grass drops, seed packets, chest loot, and natural patches. World generation and chest loot only affect new content, so old worlds may need starter items, seed packets, or admin seeding.
"""))
    for cid in ["LETTUCE", "ONION", "CORN", "TOMATO", "RICE"]:
        add(f"gardening/{slug(cid)}.md", crop_page(cid))
    add("gardening/plant-types.md", page("Plant Types", """
Plant types define the physical block behavior behind a crop. Pick the type that matches how the crop should exist in the world, not only how the final display should look.

| Type | Used By | Placement | Practical Notes |
| --- | --- | --- | --- |
| `SHORT_PLANT` | Lettuce | Ground plant on valid soil | Best default for simple crops |
| `ALLIUM` | Onion | Flower-style ground plant | Useful for small vegetable visuals |
| `TALL_PLANT` | Corn | Tall visual crop with vertical room | Needs space above the base block |
| `VINE` | Tomato, grapes | Wall-attached vine | Needs a face to attach to; poor fit for random flat patches |
| `AQUATIC` | Rice | Soil under water | Needs water setup and should be tested in claims |
| `BUSH` | Addon/extended crops | Bush-style blocks | Good for berry-like crops |
| `HANGING` | Addon/extended crops | Ceiling-attached blocks | Best for decorative or cave crops |

Plant types are data-driven, but every type still depends on Minecraft block rules. If a crop uses a real plant block, protection plugins and physics can affect it.
"""))
    packets = SEEDS.get("seed_packets", {})
    packet_rows = []
    for pid, cfg in packets.items():
        seeds = ", ".join(f"`{s['item_id']}` ({s.get('weight', 1)})" for s in cfg.get("seeds", []))
        packet_rows.append([f"`{pid}`", cfg.get("description", ""), f"{cfg.get('drops_min')}-{cfg.get('drops_max')}", seeds])
    add("gardening/seed-packets.md", page("Seed Packets", f"""
Seed packets are custom items that roll weighted seeds when opened. They are useful when you want survival discovery without requiring every crop to drop from grass.

{table(["Packet", "Description", "Drops", "Weighted contents"], packet_rows)}

Players open packets by using the item. If their inventory is full, extra seeds drop nearby.

## Design Advice

Use seed packets for starter kits, market crates, quest rewards, and rare biome crops. Keep the drop count small if packets are common, otherwise a single packet can skip the early farming loop.
"""))
    add("gardening/wild-discovery.md", page("Wild Discovery And Loot", """
`seed_acquisition.json` controls non-command crop discovery.

## Grass Drops

Grass drops use a base chance plus biome modifiers. The bundled config makes lettuce and onion common in plains/meadows, tomato more common in forests, corn more common in plains/savanna, and rice more common in swamp/jungle-style areas.

## Chest Loot

Village, farm, dungeon, mineshaft, and temple loot tables can receive Heirloom crop items or seed packets. The chance is per generated chest, not a guarantee for every structure.

## World Generation

Natural patches are placed in new chunks only. Ground crops are the safest candidates. Vine crops need walls, and aquatic crops need water placement, so test those carefully before enabling broad worldgen.

!!! warning
    World generation and chest loot only affect newly generated or newly filled content. Use commands, seed packets, or custom events if you need to seed old worlds.
"""))
    add("gardening/ecoenchants.md", page("EcoEnchants Integration", """
Heirloom reads enchantment integration data from `enchantment_integrations.json` and resolves registered Bukkit enchantments by namespaced key.

## Bundled EcoEnchants Hooks

| Purpose | Keys | Behavior |
| --- | --- | --- |
| Force replant | `ecoenchants:replant`, `ecoenchants:replenish` | Crop resets after harvest even when it would normally be removed |
| Fortune bonus | `ecoenchants:prospector` | Adds +1 effective Fortune per enchantment level |

## How This Affects Players

A replant enchantment makes farming smoother but still respects whether the crop is mature and harvestable. A Fortune bonus improves configured drop rolls; it does not invent drops that the crop JSON never defines.

## Server Owner Notes

You can add other enchantment keys in the same `namespace:name` format. After editing, reload and harvest a mature test crop with the enchanted tool to confirm the integration is detected.
"""))


def food_system_pages():
    add("food-systems/index.md", page("Food Systems", """
Heirloom food is more than hunger points. Items can carry quality, dietary labels, food properties, potion effects, creator data, consume returns, and visual IDs.

## The Important Distinction

- Dietary properties answer "what is this food made from?" Examples: vegan, vegetarian, gluten-free.
- Food properties answer "what happens when I eat this?" Examples: golden, chorus, sweet, energizing.
- Quality answers "how well did this food turn out?"

These systems can overlap on one item. A high-quality vegan food can also be `GOLDEN`, `CHORUS`, and a player's favourite food.
"""))
    props = DIET.get("dietary_properties", {})
    prop_rows = []
    for pid, cfg in props.items():
        prop_rows.append([f"`{pid}`", cfg.get("display_name", ""), cfg.get("description", ""), ", ".join(f"`{p}`" for p in cfg.get("implies", []))])
    add("food-systems/dietary-properties.md", page("Dietary Properties", f"""
Dietary labels use a blacklist model. A recipe is assumed to satisfy a property unless one of its ingredients violates that property.

{table(["Property", "Display", "Meaning", "Implies"], prop_rows)}

## How Calculation Works

When a recipe is previewed or crafted, Heirloom checks the selected ingredients. Vanilla ingredients are compared against dietary config. Custom ingredients can already carry stored dietary data, so a later recipe does not need to know every raw ingredient that originally created them.

## Inheritance Example

If a custom sauce was made with milk, and that sauce is later used in a sandwich, the sandwich should not become vegan just because the sandwich recipe only sees `SAUCE`. Stored dietary data keeps that history attached to the ingredient.

## Hierarchy

`hierarchy_rules` hide weaker labels when a stronger label is present. Bundled data treats `VEGAN` as implying `VEGETARIAN`, so vegan foods do not need to show both labels.

## Contains Lines

The `contains_settings` block controls "Contains:" lore. Use it for practical warnings, not just marketing labels. It is most useful for common allergens, roleplay restrictions, or server-specific diet rules.
"""))
    add("food-systems/food-properties.md", page("Food Properties", """
Food properties are gameplay tags stored on the item. They are not just wiki categories: when you eat the item, Heirloom loops over every stored property and applies the matching behavior.

## Where Properties Come From

A property can be added by a recipe action, usually `ADD_METADATA` with key `food_property`, or it can already exist on an ingredient. When a recipe finishes, Heirloom starts with properties already on the output, then adds every property found on every input item. The result is stored back on the output and shown in lore.

That means properties can stack through recipe chains.

## Worked Example: Powerful Pancakes

1. Make jam in the Boiling Pot with `CHORUS_FRUIT`. The jam rule adds `CHORUS`.
2. Make another jam with `GOLDEN_APPLE`. The jam rule adds `GOLDEN`.
3. Use property-bearing jam as a pancake topping in the Frying Pan. Pancakes inherit the jam's stored properties.
4. Eat the pancakes. The food applies every stored food property, then any JSON-defined effects, then favourite-food effects if pancakes are your favourite.

In bundled data, honey pancakes add honey naming, quality, and bottle return behavior. Honey does not add `SWEET` to pancakes unless a recipe or custom item explicitly stores `SWEET` as a food property. Server owners can add that behavior with recipe actions.

## Exact Property Effects

| Property | Effect when eaten |
| --- | --- |
| `GLOWING` | Glowing I for 30 seconds, beacon-style sound/message |
| `GOLDEN` | Regeneration II for 5 seconds and Absorption I for 2 minutes |
| `CHORUS` | Attempts a safe random teleport, like chorus fruit |
| `SWEET` | Speed I and Haste I for 10 seconds |
| `SPICY` | Fire Resistance I for 20 seconds, plus 1 second of visual fire |
| `COLD` | Slowness I for 5 seconds and Resistance II for 10 seconds |
| `ENERGIZING` | Speed II, Haste II, and Jump Boost I for 30 seconds |
| `NOURISHING` | Saturation III for 5 seconds |
| `HEALING` | Instant Health II |
| `AFFINITY` | If cooked by another player, Regeneration I for 10 seconds; Regeneration II if it is also your favourite food |
| `SOBERING` | If Distillery is loaded and inebriation is enabled, drains drunkenness by the configured amount, default 15 |

## What Players See

The recipe browser preview can show food-property lore based on the selected ingredients. Finished items also carry the property lore. If the final food is placed as a serving food, the placed block stores the properties too, so bites can still apply the behavior.

## Server Owner Pattern

Use properties for intentional power chains. For example, a server could make maple syrup add `SWEET`, then pancakes made with `GOLDEN` jam and syrup would carry both the inherited jam property and the syrup property.

```json
{
  "type": "ADD_METADATA",
  "key": "food_property",
  "value": "SWEET"
}
```

Avoid relying on hidden balance. If a food should heal, sober, teleport, energize, or become a strong favourite-food candidate, put that behavior in the recipe or ingredient data.
"""))
    add("food-systems/quality-and-effects.md", page("Quality And Effects", """
Quality is stored on custom foods and ingredients. Crops can preserve and improve quality, recipes can set or add quality, and mastery can improve final results.

## Quality Sources

- `SET_QUALITY` gives an output a specific value.
- `ADD_QUALITY` increases the current value when a rule matches.
- If no explicit quality is supplied, crafted custom foods can inherit the best numeric quality from their inputs.
- Cooking Mastery adds a recipe-specific quality bonus to future crafts.
- Crops can store quality and keep it when replanted.

## Effect Sources

An eaten item can apply effects from:

- Its normal food value and saturation.
- Its `food_property` tags.
- Its JSON `effects` list.
- Favourite food behavior.
- Cooked-by social behavior.
- Distillery sobering integration if `SOBERING` is present.

## Debugging Balance

If a food is too weak, check whether the recipe actually adds a property or effect. If it is too strong, check inherited ingredients first; an intermediate item may be carrying properties into many later recipes.

Prepared foods should follow configured values. If a food needs regeneration, saturation, or another potion effect, define it explicitly in JSON.
"""))
    add("food-systems/favourite-social.md", page("Favourite And Social Bonuses", """
Favourite food and cooked-by metadata are player-data systems. They are separate from recipe matching, but they can combine with food properties at eating time.

## Favourite Food

Players choose a favourite with `/hl favourite`. Eating that custom food grants:

| Effect | Duration | Strength |
| --- | --- | --- |
| Regeneration | 30 seconds | I |
| Saturation | 15 seconds | II |
| Luck | 60 seconds | I |

The favourite check runs after food-property effects. A property-stacked favourite therefore applies both sets of behavior.

## Cooked By

When a player crafts edible output, Heirloom can store the crafter UUID. Later, favourite-food checks can reward the cook with a short regeneration effect if somebody else eats the favourite food they made.

## Affinity

`AFFINITY` also reads cooked-by metadata. If the food was cooked by someone else, it grants regeneration to the eater. If that same food is also the eater's favourite, the regeneration amplifier is increased.

## Data Storage

Player RPG data is saved under `plugins/Heirloom/playerdata/`. Favourite choice and mastery are stored per player.
"""))


def server_owner_pages():
    add("server-owners/index.md", page("Server Owner Guide", """
This section is for setup, permissions, diagnostics, claim protection, localization, updates, and operational safety.
"""))
    add("server-owners/configuration.md", page("Configuration", """
Core files live in `plugins/Heirloom/` after first startup.

| File | Purpose |
| --- | --- |
| `config.yml` | License key and locale |
| `custom_items.json` | Core item definitions |
| `recipes.json` | Core recipes |
| `crops.json` | Core crops |
| `dietary_properties.json` | Diet labels and hierarchy |
| `seed_acquisition.json` | Seed packets, grass drops, loot, world patches |
| `advancements.json` | Advancement definitions |
| `enchantment_integrations.json` | EcoEnchants and compatible enchantment keys |
| `lang/<locale>.yml` | Locale files |

Run `/hl reload` after supported JSON and language changes. Restart after jar, dependency, or large visual-pack changes.
"""))
    add("server-owners/permissions.md", page("Permissions", """
Use a permission plugin such as LuckPerms on production servers.

See [Permission Reference](../reference/permissions.md) for the full list.

Recommended default grants:

```text
/lp group default permission set heirloom.use true
/lp group default permission set heirloom.recipes true
/lp group default permission set heirloom.cookbook true
/lp group default permission set heirloom.advancements true
/lp group default permission set heirloom.favourite true
/lp group default permission set heirloom.mastery true
```

Grant crop permissions if you keep the bundled crop permission nodes enabled.
"""))
    add("server-owners/commands.md", page("Commands", """
Core uses `/hl` or `/heirloom`. Distillery uses `/hld`. Cafe uses `/hlc`.

The full command list is in [Command Reference](../reference/commands.md).

## Admin Commands To Know

```text
/hl reload
/hl cheat
/hl give <item> [amount]
/hl debug test
/hld devmode status
/hlc list
```
"""))
    add("server-owners/language-files.md", page("Language Files", """
Heirloom bundles many locale files. Set the active locale in `config.yml`.

```yml
locale: en
```

Useful commands:

```text
/hl lang list
/hl lang missing <locale>
```

When making a custom translation, copy `lang/en.yml`, keep keys unchanged, translate only values, then run `/hl reload`.
"""))
    add("server-owners/region-protection.md", page("Region Protection", """
Heirloom uses two layers for protection compatibility.

## WorldGuard

- Cooking station interaction checks WorldGuard `INTERACT`.
- Planting and harvesting checks WorldGuard `BUILD`.

## Generic Claim Plugins

Planting fires a programmatic `BlockPlaceEvent`; harvesting fires a programmatic `BlockBreakEvent`. This gives plugins such as Towny, GriefPrevention, Lands, and similar systems a normal event to cancel.

## Test Before Launch

In a protected region, test:

- Planting a crop.
- Harvesting a crop.
- Using a cooking station.
- Breaking a station with ingredients.
"""))
    add("server-owners/diagnostics.md", page("Diagnostics", """
Use diagnostics after install, after updates, and after large config edits.

```text
/hl debug test
/hl debug runtests
/hl debug testall
```

The diagnostic suite checks item registry counts, cooked-rice recipe matching, crop registration, WorldGuard hook state, EcoEnchants detection, event bypass safety, and runtime GUI loading.

Other debug tools:

```text
/hl debug hunger
/hl debug actionbar <style>
```
"""))
    add("server-owners/updating.md", page("Updating And Migration Notes", """
## 2.5 Notes

- Startup banners are standardized and quieter.
- Recipe search is available through `/hl search`.
- Nexo and ItemsAdder visual resolution now share provider-neutral visual IDs.
- Prepared foods should no longer receive hidden hardcoded regeneration or bonus saturation.
- Onion and Allium crop content are bundled.
- Distillery grape crop definitions are restored.

## 2.0 Notes

- Region protection was rewritten around WorldGuard and standard Bukkit events.
- Generic `consume_return` was added.
- EcoEnchants replant and prospector hooks were added.
- Seed packets and world discovery were added.
- Native advancements, mastery, and favourite food systems were expanded.

## Update Checklist

1. Back up `plugins/Heirloom/`.
2. Stop the server.
3. Replace jars.
4. Start and read startup warnings.
5. Run `/hl debug test`.
6. Review custom food balance if you previously worked around hidden effects.
"""))


def customization_pages():
    add("customization/index.md", page("Customization", """
Heirloom content is mostly data-driven. Server owners can customize items, recipes, crops, diet labels, seed acquisition, advancements, and visual mappings.

## Recommended Workflow

1. Make one small JSON change.
2. Validate the file syntax.
3. Run `/hl reload` when the file supports reload.
4. Search the item or recipe in game.
5. Craft it once and inspect the output lore.
6. Only then build the next step of the chain.

This matters because Heirloom recipes can carry metadata forward. A mistake in an intermediate ingredient can affect every later recipe that uses it.
"""))
    add("customization/custom-foods.md", page("Custom Foods", """
Custom foods are defined in JSON under `custom_items` arrays. A custom food defines the item players can hold; recipes define how players make it.

## Minimum Edible Food

```json
{
  "id": "GOLDEN_PANCAKE",
  "name": "Golden Pancake",
  "base_material": "PLAYER_HEAD",
  "texture": "http://textures.minecraft.net/texture/...",
  "edible": true,
  "food_value": 8,
  "saturation": 6.0,
  "consume_seconds": 1.4,
  "animation": "EAT",
  "visual_id": "GOLDEN_PANCAKE"
}
```

## Advanced Fields To Know

- `consume_return`: gives an item back after eating.
- `placeable_servings`: makes the food placeable and eaten in servings.
- `feast`: enables shared-feast behavior.
- `effects`: applies explicit potion effects when eaten.
- `visual_id`: lets Nexo or ItemsAdder replace the visual without changing recipes.

## Common Mistakes

- Defining an item but never adding a recipe for it.
- Using a pretty `name` but forgetting the stable uppercase `id` used in recipes.
- Expecting a property effect without adding a recipe action or stored property.
- Using provider-specific visual IDs instead of stable Heirloom visual IDs.

## How To Test

Use `/hl give <id>` to inspect the item definition, then craft it through the intended recipe to inspect inherited quality, properties, and returns.
"""))
    add("customization/custom-recipes.md", page("Custom Recipes", """
Recipes define a station, output, processing time, ingredients, actions, and optional rules. The output can be changed by base actions, rule actions, inherited input metadata, and quality logic.

## Minimum Recipe

```json
{
  "id": "SWEET_PANCAKES",
  "station": "FRYING_PAN",
  "output": "PANCAKES",
  "processing_time": 160,
  "ingredients": [
    { "type": "REQUIRED", "max": 1, "options": [{ "custom_item": "BAG_OF_FLOUR" }] },
    { "type": "REQUIRED", "max": 1, "options": [{ "item": "EGG" }] },
    { "type": "OPTIONAL", "max": 1, "options": [{ "item": "HONEY_BOTTLE" }] }
  ],
  "actions": [
    { "type": "SET_PROPERTY", "key": "NAME", "value": "Sweet Pancakes" },
    { "type": "ADD_METADATA", "key": "food_property", "value": "SWEET" }
  ]
}
```

## Advanced Pattern: Property Chain

Put properties on intermediate ingredients when you want players to build stronger food through multiple steps. For example, jam can get `CHORUS` from chorus fruit, then pancakes inherit that property when the jam is used as a topping.

## Common Rule Actions

- `SET_PROPERTY` with key `NAME`: changes display name.
- `ADD_METADATA` with key `food_property`: adds a food property that can be inherited and applied when eaten.
- `SET_RETURN_ITEM`: returns a container when crafting completes.
- `SET_CONSUME_RETURN`: returns a container after eating.
- `SET_VISUAL_ITEM`: swaps to a provider-neutral visual variant.
- `ADD_QUALITY` and `SET_QUALITY`: tune output quality.

## Common Mistakes

- Using `SET_PROPERTY` for `food_property`; bundled property recipes use `ADD_METADATA` for inherited food properties.
- Putting a custom item in `item` instead of `custom_item`.
- Forgetting that optional slots default to `0-max`, so rules must handle the missing-input case.
- Editing JSON and testing only `/hl give`; recipe actions and inheritance only appear when the recipe is crafted.

## How To Test

Run `/hl reload`, search the recipe, craft every branch you changed, and inspect lore. For inheritance tests, craft the intermediate ingredient first, then use that exact item in the next recipe.
"""))
    add("customization/custom-crops.md", page("Custom Crops", """
Crop JSON defines plant type, growth behavior, planting rules, textures, and harvest drops.

## Minimum Crop Shape

A crop needs an item ID, plant type, growth settings, planting rules, textures, and harvest rules. Use an existing crop close to your desired behavior as the starting point: lettuce for ground crops, tomato for vines, rice for aquatic crops, corn for tall crops.

## Important Sections

- `growth`: duration, variance, stages, and scale.
- `planting`: valid blocks, item consumption, and permission.
- `textures`: growing and ripe display textures.
- `harvest`: drops, bonus drops, replanting, sounds, and quality chance.

## Design Choices

Choose a plant type based on physical behavior. A tomato-like crop should be a vine because it needs a wall. A rice-like crop should be aquatic because the water requirement is part of gameplay. Do not use a display offset to fake a crop type that has different block rules.

## Common Mistakes

- Enabling world generation for a vine crop without natural wall positions.
- Giving aquatic crops to players before they know the water placement rule.
- Adding bonus drops that require Fortune, then testing with an unenchanted tool.
- Forgetting crop permissions when planting works for admins but not players.

## How To Test

Plant it, wait or speed up growth, harvest it, confirm drops, confirm replanting, then test in a protected region with a normal player.
"""))
    add("customization/seed-acquisition.md", page("Seed Acquisition", """
`seed_acquisition.json` controls how crops enter survival gameplay.

Use it to configure:

- Seed packets.
- Grass drops.
- Chest loot injection.
- Natural world patches.

## Balancing Advice

Use grass drops for common crops, seed packets for curated rewards, chest loot for exploration, and world patches for discovery. Avoid enabling all methods at high rates or rare crops stop feeling rare.

Keep world-generation changes conservative on live servers. They only affect new chunks and can make rare crops too common if patch chances are high.
"""))
    add("customization/advancements.md", page("Advancements", """
`advancements.json` controls Heirloom advancement definitions. Advancements can track foods eaten, crops harvested, quality milestones, and recipe progress.

## Useful Advancement Shapes

- First-time milestones teach players that a system exists.
- Collections encourage recipe exploration.
- Quality goals reward farming and mastery.
- Counters reward repeated cooking or harvesting.

After editing, run `/hl reload` and test with `/hl advancements`.
"""))
    add("customization/visuals-overview.md", page("Visual Integrations Overview", """
Heirloom works without a resource pack by using vanilla materials and player-head textures. Optional providers can replace that presentation.

## Provider-Neutral Flow

1. Item definitions declare `visual_id`.
2. Recipes can call `SET_VISUAL_ITEM`.
3. `VisualItemResolver` asks registered providers for that visual.
4. If no provider has it, Heirloom falls back to the normal item.

This keeps recipe data independent from Nexo or ItemsAdder.

## Practical Rule

Use Heirloom item IDs and visual IDs as stable public names. Let Nexo or ItemsAdder map those names to models. Do not bake a provider namespace into a recipe unless you want that recipe to stop being portable.
"""))
    add("customization/nexo.md", page("Nexo Integration", """
Nexo is a soft dependency. Heirloom should load without it.

## Recommended Mapping

Create Nexo items that match Heirloom visual IDs. A common naming convention is:

```text
heirloom_<lowercase_visual_id>
```

Examples:

```text
heirloom_tomato
heirloom_ice_cream_chorus
heirloom_espresso
```

## Testing

Start the server with Nexo installed, run `/hl reload`, then create the item through Heirloom rather than directly through Nexo. That proves the provider path is being used by recipes and commands.
"""))
    add("customization/itemsadder.md", page("ItemsAdder Integration", """
ItemsAdder is a soft dependency. Heirloom uses the same logical `visual_id` path for ItemsAdder as it does for Nexo.

## Recommended Mapping

Create ItemsAdder custom stacks for the visual IDs your server wants to replace. Keep IDs stable so recipe actions such as `SET_VISUAL_ITEM` do not need to change.

## Fallback Rule

If ItemsAdder is missing or an item is not mapped, the normal Heirloom item is still created. Test this fallback before launch so players are not blocked by a visual-pack mistake.
"""))
    add("customization/web-generator.md", page("Web Generator Workflow", """
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
"""))


def addons_pages():
    add("addons/distillery/index.md", page("Distillery Addon", f"""
{image("../../images/distillery-banner.svg", "Distillery adds multi-stage brewing, fermentation, distillation, traits, and inebriation.")}

Distillery depends on Heirloom core. It adds grapes, mashables, stomping, wort, must, fermentation, distillation, named drink profiles, traits, and drunkenness systems.

Distillery is not just a recipe pack. It has its own processing stations and metadata, then connects back into Heirloom through registered items, crops, commands, and the `SOBERING` food property.

Start with [Getting Started](getting-started.md), then read [Brewing Flow](brewing-flow.md).
"""))
    add("addons/distillery/getting-started.md", page("Distillery Getting Started", """
1. Install Heirloom core.
2. Install HeirloomDistillery.
3. Restart the server.
4. Confirm `/hld help` works.
5. Get starter items with `/hld list` and `/hld give <item> [amount]`.

Players begin by collecting mashable ingredients, using the Stomping Tub, then moving liquid through fermentation and distillation.

## First Successful Flow

Use a simple fruit path first: collect grapes, stomp them into must, ferment the must, then inspect the finished drink. After that, try grain wort, because grain adds the extra Boiling Pot step before fermentation.
"""))
    add("addons/distillery/brewing-flow.md", page("Distillery Brewing Flow", f"""
{image("../../../images/distillery/D_mashing_fruit.gif", "Fruit and grain processing starts with mashing or stomping.")}

## Main Flow

1. Mash or stomp ingredients.
2. Branch by ingredient profile.
3. Ferment fruit must, or boil grain wort before fermentation.
4. Distill stronger spirits when the drink type supports it.
5. Inspect traits, ABV, and quality.

## Fruit Vs Grain

Fruit must is ready for fermentation after crushing. Grain wort needs the Boiling Pot first, then fermentation. This is the most common player confusion, so use `/hld stats <item>` and item lore when teaching the addon.

## Metadata Matters

Distillery drinks preserve metadata through custom output handlers. Ingredients, traits, ABV, and quality are part of the item identity, not just the display name.
"""))
    add("addons/distillery/mashables-traits.md", page("Mashables And Traits", """
Mashables have brewing stats such as sugar, tannin, and acidity. Distillery uses those stats to shape output quality and drink identity.

## What Traits Do

Traits are discoverable properties that make drinks feel different beyond a simple item ID. Some traits come from ingredient counts, purity, fruit choices, or special combinations.

## How To Explore

Use `/hld stats <item>` before brewing. It shows whether an ingredient leans sweet, tannic, acidic, grain-like, or special. Then compare the finished drink lore after fermentation or distillation.

Admins tune mashables in Distillery config/resource files.
"""))
    add("addons/distillery/inebriation.md", page("Inebriation", """
Distillery tracks drunkenness separately from ordinary food. Drinks can raise a player's level, affect chat through slurring rules, and trigger blackout or wakeup behavior depending on configuration.

Useful commands:

```text
/hld drunk
/hld setdrunk <player> <level>
/hld adddrunk <player> <amount>
/hld wakeup list
```

## Sobering Food

The Heirloom `SOBERING` food property connects back into Distillery. When Distillery is loaded and inebriation is enabled, eating a food with `SOBERING` drains drunkenness by the configured amount, default 15.

Use this for server foods such as strong coffee, greasy meals, or custom hangover cures.
"""))
    add("addons/distillery/configuration.md", page("Distillery Configuration", """
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
"""))
    add("addons/distillery/commands-permissions.md", page("Distillery Commands And Permissions", """
Use `/hld`.

| Command | Purpose | Permission |
| --- | --- | --- |
| `/hld help` | Help | `heirloom.distillery.use` |
| `/hld info` | Addon info | `heirloom.distillery.use` |
| `/hld menu` | Distillery GUI | `heirloom.distillery.use` |
| `/hld list` | List items | `heirloom.distillery.use` |
| `/hld stats <item>` | Ingredient stats | `heirloom.distillery.use` |
| `/hld drunk [player]` | Drunkenness level | self use, others admin |
| `/hld give <item> [amount]` | Give items | `heirloom.distillery.admin` |
| `/hld reload` | Reload | `heirloom.distillery.admin` |
| `/hld devmode [on|off|status]` | Fast processing mode | `heirloom.distillery.admin` |
| `/hld lab` | Brew Lab | `heirloom.distillery.admin` |
"""))
    add("addons/cafe/index.md", page("Cafe Addon", """
Cafe is a stable Heirloom addon in the default build profile. It adds coffee cherries, coffee roasting, tea processing, oat milk, espresso drinks, cocoa, boba, iced coffee, and the Barista Machine.

Cafe content registers into the normal Heirloom recipe browser, but the final drink assembly uses the Cafe Barista Machine.

Use `/hlc help` for addon commands.
"""))
    add("addons/cafe/getting-started.md", page("Cafe Getting Started", """
1. Install Heirloom core.
2. Install HeirloomCafe.
3. Restart the server.
4. Confirm `/hlc help` works.
5. Build a Barista Machine: iron trapdoor above quartz stairs.

Core station recipes handle roasting and grinding. Barista Machine recipes handle drink assembly.

## First Successful Flow

Roast coffee cherries into beans, pull espresso, then make an americano. That proves the Oven chain, the Barista Machine, and drink assembly before you add milk variants.
"""))
    add("addons/cafe/barista-machine.md", page("Barista Machine", """
The Barista Machine is Cafe's signature station.

Build:

```text
IRON_TRAPDOOR
QUARTZ_STAIRS
```

The iron trapdoor is the shared station anchor. Clicking either part resolves to the same station when Cafe is registered.

## What Belongs Here

Use the Barista Machine for finished drinks: espresso, americano, lattes, cappuccino, mocha, teas, cocoa, boba, and iced coffee. Use core stations for earlier prep such as roasting beans or grinding leaves.
"""))
    add("addons/cafe/coffee-tea.md", page("Coffee And Tea Flow", """
Cafe adds several chains:

- Coffee cherry -> light beans -> medium beans -> dark beans.
- Medium/dark beans -> espresso.
- Espresso + water -> americano.
- Espresso + milk/oat milk -> latte, cappuccino, flat white, mocha.
- Leaves -> leaf litter or dried green tea.
- Dried green tea -> chance at matcha powder.
- Tea leaves -> green tea, black tea, sweet tea, matcha latte.
- Tea + milk + sugar + boba ingredient -> boba tea.

## Core Stations Vs Cafe Station

The Oven and prep stations create the ingredients. The Barista Machine assembles the drinks. If a player tries to make a latte before pulling espresso, the recipe is missing an intermediate, not a permission.

## Ingredient Variants

Milk bucket and oat milk variants can change names, returns, and dietary behavior. Sweet or glow berry variants can change drink identity when the recipe has a matching rule.

See [Default Recipe Index](../../recipes/default-recipes.md) for exact recipes and links.
"""))
    add("addons/cafe/configuration.md", page("Cafe Configuration", """
Cafe writes editable resources to `plugins/HeirloomCafe/`:

- `custom_items-cafe.json`
- `crops-cafe.json`
- `recipes-cafe.json`
- `config.yml`
- `lang/en.yml`

Cafe unregisters and re-registers its addon-owned items, crops, and recipes on reload callbacks so the recipe browser can refresh.

## Test After Changes

After recipe edits, run `/hl reload`, search for `cafe`, then test one coffee chain and one tea chain. That catches both core-station prep and Barista Machine assembly.
"""))
    add("addons/cafe/commands-permissions.md", page("Cafe Commands And Permissions", """
Use `/hlc` for Cafe-specific addon commands. Cafe recipes also appear in the normal Heirloom `/hl` recipe browser.

| Command | Purpose | Permission |
| --- | --- | --- |
| `/hlc help` | Help | `heirloom.cafe.use` |
| `/hlc list` | List Cafe items | `heirloom.cafe.use` |
| `/hlc give <item> [amount]` | Give Cafe items | `heirloom.cafe.admin` |
| `/hlc reload` | Reload Cafe resources | `heirloom.cafe.admin` |

## Practical Notes

Players usually only need the normal Heirloom menu and recipe search. Admins use `/hlc list` and `/hlc give` while testing Cafe item IDs, then `/hl reload` or the addon reload path after resource edits.
"""))


def reference_pages():
    add("reference/index.md", page("Reference", """
Reference pages are for exact IDs, commands, permissions, and JSON fields. Use guide pages first when learning a system.
"""))
    add("reference/items.md", build_item_reference())
    add("reference/vanilla-items.md", build_vanilla_item_reference())
    add("reference/crops.md", build_crop_reference())
    add("reference/recipes.md", build_recipe_reference())
    add("reference/visual-ids.md", build_visual_reference())
    add("reference/commands.md", page("Command Reference", """
## Core

| Command | Purpose | Permission |
| --- | --- | --- |
| `/hl` | Open main menu | `heirloom.use` |
| `/hl help` | Help | `heirloom.use` |
| `/hl cookbook` | Give recipe book | `heirloom.cookbook` |
| `/hl recipes` | Recipe browser | `heirloom.recipes` |
| `/hl search <query>` | Recipe search | `heirloom.recipes` |
| `/hl advancements` | Advancement progress | `heirloom.advancements` |
| `/hl favourite` | Favourite food GUI | `heirloom.favourite` |
| `/hl mastery` | Cooking mastery | `heirloom.mastery` |
| `/hl list <items|recipes|dietary>` | List content | `heirloom.use` |
| `/hl give <item> [amount]` | Give item | `heirloom.give` |
| `/hl cheat` | Admin item GUI | `heirloom.cheat` |
| `/hl reload` | Reload supported data | `heirloom.reload` |
| `/hl lang list` | Locale list | `heirloom.reload` |
| `/hl lang missing <locale>` | Missing locale keys | `heirloom.reload` |
| `/hl debug test` | Diagnostics | `heirloom.debug` |
| `/hl cleanup [radius]` | Remove orphan entities | `heirloom.admin` |

## Addons

See [Distillery Commands](../addons/distillery/commands-permissions.md) and [Cafe Commands](../addons/cafe/commands-permissions.md).
"""))
    crop_perm_rows = []
    for crop in sorted([c for c in CROPS if c["_source"] == "Core"], key=lambda c: c.get("id", "")):
        perm = crop.get("planting", {}).get("permission")
        if perm:
            crop_perm_rows.append([f"`{perm}`", crop.get("id", "")])
    add("reference/permissions.md", page("Permission Reference", f"""
## Core

| Permission | Default | Purpose |
| --- | --- | --- |
| `heirloom.use` | true | Basic access |
| `heirloom.cookbook` | true | Recipe book command |
| `heirloom.recipes` | true | Recipe browser and search |
| `heirloom.advancements` | true | Advancement GUI |
| `heirloom.favourite` | true | Favourite food GUI |
| `heirloom.mastery` | true | Mastery GUI |
| `heirloom.give` | op | Give custom items |
| `heirloom.cheat` | op | Cheat item GUI |
| `heirloom.reload` | op | Reload data and language diagnostics |
| `heirloom.debug` | op | Debug tools |
| `heirloom.admin` | op | Parent admin node |

## Crop Planting

{table(["Permission", "Crop"], crop_perm_rows)}

## Addons

| Permission | Default | Purpose |
| --- | --- | --- |
| `heirloom.distillery.use` | true | Distillery commands and menus |
| `heirloom.distillery.admin` | op | Distillery admin tools |
| `heirloom.cafe.use` | true | Cafe commands |
| `heirloom.cafe.admin` | op | Cafe item give |
"""))
    add("reference/config-files.md", page("Configuration Files", """
| File | Plugin | Purpose |
| --- | --- | --- |
| `config.yml` | Core | License and locale |
| `custom_items.json` | Core | Main items |
| `custom_items-world.json` | Core | World food items |
| `custom_items-festive.json` | Core | Seasonal foods |
| `recipes.json` | Core | Main recipes |
| `recipes-world.json` | Core | World recipes |
| `recipes-festive.json` | Core | Seasonal recipes |
| `crops.json` | Core | Core crops |
| `crops-distillery.json` | Core/addon data | Distillery grape crops |
| `dietary_properties.json` | Core | Diet labels |
| `seed_acquisition.json` | Core | Seeds and world discovery |
| `enchantment_integrations.json` | Core | EcoEnchants hooks |
| `custom_items-cafe.json` | Cafe | Cafe items |
| `recipes-cafe.json` | Cafe | Cafe recipes |
| `crops-cafe.json` | Cafe | Coffee crop |
| `ingredients.yml` | Distillery | Mashables and processing settings |
| `words.yml` | Distillery | Slur replacements |
"""))
    add("reference/recipe-actions-rules.md", page("Recipe Actions And Rules", """
Recipe actions modify output after a recipe matches.

| Action | Purpose |
| --- | --- |
| `SET_PROPERTY` | Set metadata such as display name or `food_property` |
| `ADD_QUALITY` | Add quality to output |
| `SET_QUALITY` | Set output quality |
| `SET_TEXTURE` | Change player-head texture |
| `SET_VISUAL_ITEM` | Swap output to a provider-neutral visual item |
| `SET_RETURN_ITEM` | Return a container such as `BUCKET` |
| `SET_CONSUME_RETURN` | Store return metadata for later consumption/use |

Common triggers include `HAS_INPUT`, `HAS_ANY_INGREDIENT`, `HAS_ALL_INGREDIENTS`, `HAS_INGREDIENT_PROPERTY`, `HAS_ALL_INGREDIENT_PROPERTIES`, and `INPUT_COUNT_GTE`.
"""))
    add("reference/json-fields.md", page("JSON Field Reference", """
## Custom Item Fields

| Field | Meaning |
| --- | --- |
| `id` | Stable uppercase item ID |
| `name` | Display name |
| `base_material` | Vanilla base material |
| `texture` | Player-head texture URL |
| `edible` | Whether the item can be consumed |
| `food_value` | Hunger restored |
| `saturation` | Saturation restored |
| `consume_seconds` | Consume duration |
| `animation` | `EAT` or `DRINK` style animation |
| `effects` | Potion effects |
| `visual_id` | Provider-neutral visual lookup key |
| `consume_return` | Item returned after consumption or recipe use |
| `placeable_servings` | Cake-like serving count |
| `feast` | Enables feast participant behavior |

## Recipe Fields

| Field | Meaning |
| --- | --- |
| `id` | Stable recipe ID |
| `station` | Cooking station |
| `output` | Main output item |
| `weighted_outputs` | Chance-based output list |
| `processing_time` | Ticks |
| `ingredients` | Required/optional slots |
| `actions` | Always-applied output changes |
| `rules` | Conditional output changes |

## Crop Fields

| Field | Meaning |
| --- | --- |
| `id` | Crop ID |
| `item_id` | Item used for planting/harvest |
| `plant_type` | Physical crop behavior |
| `growth` | Timing, scale, stages |
| `planting` | Valid blocks and permissions |
| `textures` | Growing/ripe display textures |
| `harvest` | Drops, sounds, replant, quality chance |
"""))


def legacy_path_pages():
    # Keep old URLs useful and included in nav.
    add("core/cooking-stations.md", page("Core Cooking Stations", "The station docs moved to [Cooking Stations](../stations/index.md)."))
    add("core/recipes.md", page("Core Recipes", "The recipe docs moved to [Recipes](../recipes/index.md) and the [Default Recipe Index](../recipes/default-recipes.md)."))
    add("core/custom-foods.md", page("Core Custom Foods", "The custom food docs moved to [Custom Foods](../customization/custom-foods.md) and [Item Reference](../reference/items.md)."))
    add("core/gardening.md", page("Core Gardening", "The gardening docs moved to [Gardening](../gardening/index.md)."))
    add("core/dietary-properties.md", page("Core Dietary Properties", "The dietary docs moved to [Dietary Properties](../food-systems/dietary-properties.md)."))
    add("core/visual-integrations.md", page("Core Visual Integrations", "Visual docs moved to [Visual Integrations Overview](../customization/visuals-overview.md), [Nexo](../customization/nexo.md), and [ItemsAdder](../customization/itemsadder.md)."))
    add("core/admin-configuration.md", page("Core Admin Configuration", "Server owner docs moved to [Configuration](../server-owners/configuration.md)."))
    add("distillery/overview.md", page("Distillery Overview", "Distillery docs moved to [Distillery Addon](../addons/distillery/index.md)."))
    add("distillery/getting-started.md", page("Distillery Getting Started", "Distillery docs moved to [Distillery Getting Started](../addons/distillery/getting-started.md)."))
    add("distillery/brewing-flow.md", page("Distillery Brewing Flow", "Distillery docs moved to [Brewing Flow](../addons/distillery/brewing-flow.md)."))
    add("distillery/mashables-traits.md", page("Distillery Mashables And Traits", "Distillery docs moved to [Mashables And Traits](../addons/distillery/mashables-traits.md)."))
    add("distillery/inebriation.md", page("Distillery Inebriation", "Distillery docs moved to [Inebriation](../addons/distillery/inebriation.md)."))
    add("distillery/admin-configuration.md", page("Distillery Admin Configuration", "Distillery docs moved to [Configuration](../addons/distillery/configuration.md)."))
    add("distillery/commands-permissions.md", page("Distillery Commands And Permissions", "Distillery docs moved to [Commands And Permissions](../addons/distillery/commands-permissions.md)."))
    add("reference/configuration-files.md", page("Configuration Files", "This reference moved to [Config Files](config-files.md)."))
    add("reference/customization.md", page("Customization Notes", "Customization docs moved to [Customization](../customization/index.md)."))


def build_nav() -> str:
    return """site_name: Heirloom Wiki
site_description: Wiki and server-owner manual for the Heirloom Minecraft cooking, gardening, Distillery, and Cafe plugins.
site_url: https://kernel-person.github.io/heirloom-docs/
repo_url: https://github.com/kernel-person/heirloom-docs
repo_name: kernel-person/heirloom-docs

theme:
  name: material
  language: en
  logo: images/heirloom-logo.png
  favicon: images/heirloom-logo.png
  palette:
    - scheme: default
      primary: green
      accent: deep orange
  features:
    - navigation.instant
    - navigation.instant.prefetch
    - navigation.instant.progress
    - navigation.sections
    - navigation.top
    - navigation.indexes
    - search.suggest
    - search.highlight
    - content.code.copy

extra_css:
  - stylesheets/extra.css

extra_javascript:
  - javascripts/navigation-scroll.js

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true

nav:
  - Home: index.md
  - Getting Started:
      - Installation: getting-started/installation.md
      - First Meal: getting-started/first-meal.md
      - First Farm: getting-started/first-farm.md
      - Recipe Browser: getting-started/recipe-browser.md
  - Player Guide:
      - Overview: player-guide/index.md
      - Cooking Basics: player-guide/cooking.md
      - Recipe Search: player-guide/recipe-search.md
      - Favourite Food: player-guide/favourite-food.md
      - Food Quality: player-guide/quality.md
      - Advancements: player-guide/advancements.md
      - Cooking Mastery: player-guide/mastery.md
      - Placeable Foods And Feasts: player-guide/placeable-foods.md
      - Seed Discovery: player-guide/seed-discovery.md
  - Cooking Stations:
      - Overview: stations/index.md
      - Oven: stations/oven.md
      - Boiling Pot: stations/boiling-pot.md
      - Mixing Bowl: stations/mixing-bowl.md
      - Cutting Board: stations/cutting-board.md
      - Frying Pan: stations/frying-pan.md
      - Barista Machine: stations/barista-machine.md
  - Recipes:
      - Overview: recipes/index.md
      - Default Recipe Index: recipes/default-recipes.md
      - Oven Recipes: recipes/station-oven.md
      - Boiling Pot Recipes: recipes/station-boiling-pot.md
      - Mixing Bowl Recipes: recipes/station-mixing-bowl.md
      - Cutting Board Recipes: recipes/station-cutting-board.md
      - Frying Pan Recipes: recipes/station-frying-pan.md
      - Barista Recipes: recipes/station-barista-machine.md
      - Recipe Chains: recipes/recipe-chains.md
  - Gardening:
      - Overview: gardening/index.md
      - Lettuce: gardening/lettuce.md
      - Onion: gardening/onion.md
      - Corn: gardening/corn.md
      - Tomato: gardening/tomato.md
      - Rice: gardening/rice.md
      - Plant Types: gardening/plant-types.md
      - Seed Packets: gardening/seed-packets.md
      - Wild Discovery And Loot: gardening/wild-discovery.md
      - EcoEnchants: gardening/ecoenchants.md
  - Food Systems:
      - Overview: food-systems/index.md
      - Dietary Properties: food-systems/dietary-properties.md
      - Food Properties: food-systems/food-properties.md
      - Quality And Effects: food-systems/quality-and-effects.md
      - Favourite And Social Bonuses: food-systems/favourite-social.md
  - Server Owners:
      - Overview: server-owners/index.md
      - Configuration: server-owners/configuration.md
      - Permissions: server-owners/permissions.md
      - Commands: server-owners/commands.md
      - Language Files: server-owners/language-files.md
      - Region Protection: server-owners/region-protection.md
      - Diagnostics: server-owners/diagnostics.md
      - Updating: server-owners/updating.md
  - Customization:
      - Overview: customization/index.md
      - Custom Foods: customization/custom-foods.md
      - Custom Recipes: customization/custom-recipes.md
      - Custom Crops: customization/custom-crops.md
      - Seed Acquisition: customization/seed-acquisition.md
      - Advancements: customization/advancements.md
      - Visual Integrations: customization/visuals-overview.md
      - Nexo: customization/nexo.md
      - ItemsAdder: customization/itemsadder.md
      - Web Generator: customization/web-generator.md
  - Addons:
      - Distillery:
          - Overview: addons/distillery/index.md
          - Getting Started: addons/distillery/getting-started.md
          - Brewing Flow: addons/distillery/brewing-flow.md
          - Mashables And Traits: addons/distillery/mashables-traits.md
          - Inebriation: addons/distillery/inebriation.md
          - Configuration: addons/distillery/configuration.md
          - Commands And Permissions: addons/distillery/commands-permissions.md
      - Cafe:
          - Overview: addons/cafe/index.md
          - Getting Started: addons/cafe/getting-started.md
          - Barista Machine: addons/cafe/barista-machine.md
          - Coffee And Tea Flow: addons/cafe/coffee-tea.md
          - Configuration: addons/cafe/configuration.md
          - Commands And Permissions: addons/cafe/commands-permissions.md
      - Future Addons: roadmap.md
  - Reference:
      - Overview: reference/index.md
      - Commands: reference/commands.md
      - Permissions: reference/permissions.md
      - Config Files: reference/config-files.md
      - Item IDs: reference/items.md
      - Vanilla Ingredients: reference/vanilla-items.md
      - Crop IDs: reference/crops.md
      - Recipe Summary: reference/recipes.md
      - Recipe Actions And Rules: reference/recipe-actions-rules.md
      - JSON Fields: reference/json-fields.md
      - Visual IDs: reference/visual-ids.md
      - Legacy Configuration Path: reference/configuration-files.md
      - Legacy Customization Path: reference/customization.md
  - Gallery: gallery.md
  - Media Needed: media-needed.md
  - Legacy Paths:
      - Core Cooking Stations: core/cooking-stations.md
      - Core Recipes: core/recipes.md
      - Core Custom Foods: core/custom-foods.md
      - Core Gardening: core/gardening.md
      - Core Dietary Properties: core/dietary-properties.md
      - Core Visual Integrations: core/visual-integrations.md
      - Core Admin Configuration: core/admin-configuration.md
      - Distillery Overview: distillery/overview.md
      - Distillery Getting Started: distillery/getting-started.md
      - Distillery Brewing Flow: distillery/brewing-flow.md
      - Distillery Mashables And Traits: distillery/mashables-traits.md
      - Distillery Inebriation: distillery/inebriation.md
      - Distillery Admin Configuration: distillery/admin-configuration.md
      - Distillery Commands And Permissions: distillery/commands-permissions.md
"""


def css() -> str:
    old = (DOCS_ROOT / "docs/stylesheets/extra.css").read_text(encoding="utf-8")
    marker = "/* Heirloom generated utility styles */"
    if marker in old:
        old = old.split(marker, 1)[0].rstrip()
    extra = """
/* Heirloom generated utility styles */

.md-typeset .hl-kbd {
  padding: 0.08rem 0.35rem;
  border: 1px solid var(--hl-border-strong);
  border-radius: 4px;
  background: var(--hl-inner);
  font-size: 0.78rem;
  font-weight: 700;
}

.md-typeset .hl-small {
  color: var(--hl-muted);
  font-size: 0.82rem;
}

.md-typeset .hl-card code,
.md-typeset td code {
  white-space: nowrap;
}

.md-typeset table:not([class]) {
  font-size: 0.78rem;
}

.md-typeset .hl-item-icon {
  width: 28px;
  height: 28px;
  image-rendering: pixelated;
  vertical-align: middle;
  border: 1px solid var(--hl-border-strong);
  border-radius: 4px;
  background: var(--hl-inner);
  box-shadow: 0 1px 2px var(--hl-shadow);
}

.md-typeset .hl-icon-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin: 0.08rem 0.12rem 0.08rem 0;
  line-height: 1;
}

.md-typeset .hl-input-strip,
.md-typeset .hl-recipe-slots {
  display: inline-flex;
  flex-wrap: wrap;
  gap: 0.32rem 0.42rem;
  align-items: center;
  min-width: 7rem;
}

.md-typeset .hl-ingredient-slot {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 54px;
  vertical-align: middle;
}

.md-typeset .hl-slot-box {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.22rem;
  min-height: 54px;
  min-width: 54px;
  padding: 0.14rem 0.24rem;
  border: 1px solid color-mix(in srgb, var(--hl-border-strong) 78%, white);
  border-radius: 7px;
  background: color-mix(in srgb, var(--hl-inner) 94%, white);
  box-shadow: 0 1px 2px rgba(43, 33, 24, 0.16);
}

.md-typeset .hl-recipe-slots .hl-icon-link {
  margin: 0;
}

.md-typeset .hl-recipe-slots .hl-item-icon {
  width: 48px;
  height: 48px;
  border: 0;
  border-radius: 0;
  background: transparent;
  box-shadow: none;
}

.md-typeset .hl-slot-choice-icons {
  display: inline-flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.18rem;
}

.md-typeset .hl-choice-separator {
  color: var(--hl-muted);
  font-size: 0.62rem;
  font-weight: 700;
  line-height: 1;
  text-transform: lowercase;
}

.md-typeset .hl-slot-count {
  position: absolute;
  right: 0.08rem;
  bottom: 0.08rem;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 0.88rem;
  height: 0.78rem;
  padding: 0 0.1rem;
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 3px;
  background: rgba(24, 20, 18, 0.9);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.42);
  color: #fff7e8;
  font-size: 0.54rem;
  font-weight: 900;
  line-height: 1;
  pointer-events: none;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.85);
  white-space: nowrap;
}

.md-typeset .hl-output-item {
  display: inline-flex;
  align-items: center;
  gap: 0.46rem;
  color: var(--hl-terracotta);
  font-weight: 700;
  white-space: nowrap;
}

.md-typeset .hl-output-item .hl-item-icon {
  width: 48px;
  height: 48px;
  border-color: color-mix(in srgb, var(--hl-border-strong) 78%, white);
  border-radius: 7px;
  background: color-mix(in srgb, var(--hl-inner) 94%, white);
  box-shadow: 0 1px 2px rgba(43, 33, 24, 0.16);
}

.md-typeset .hl-output-item:hover {
  text-decoration: none;
}

.md-typeset .hl-output-name code,
.md-typeset .hl-output-name {
  white-space: nowrap;
}

.md-typeset .hl-icon-missing {
  border-style: dashed;
  opacity: 0.8;
}
"""
    return old.rstrip() + "\n" + extra


def helper_script() -> str:
    return Path(__file__).read_text(encoding="utf-8")


def navigation_scroll_js() -> str:
    return """(function () {
  var NAV_SCROLLWRAP = '.md-sidebar[data-md-type="navigation"] .md-sidebar__scrollwrap';
  var rememberedScrollTop = null;
  var restorePending = false;
  var watchedScrollwrap = null;

  function getScrollwrap() {
    return document.querySelector(NAV_SCROLLWRAP);
  }

  function rememberScroll() {
    var scrollwrap = getScrollwrap();
    if (scrollwrap) {
      rememberedScrollTop = scrollwrap.scrollTop;
    }
  }

  function onSidebarScroll() {
    if (!restorePending) {
      rememberedScrollTop = this.scrollTop;
    }
  }

  function watchSidebar() {
    var scrollwrap = getScrollwrap();
    if (!scrollwrap || scrollwrap === watchedScrollwrap) {
      return;
    }
    if (watchedScrollwrap) {
      watchedScrollwrap.removeEventListener('scroll', onSidebarScroll);
    }
    watchedScrollwrap = scrollwrap;
    watchedScrollwrap.addEventListener('scroll', onSidebarScroll, { passive: true });
    if (rememberedScrollTop === null) {
      rememberedScrollTop = watchedScrollwrap.scrollTop;
    }
  }

  function isInternalLink(link) {
    if (!link || link.target || link.hasAttribute('download')) {
      return false;
    }
    var href = link.getAttribute('href') || '';
    if (!href || href.charAt(0) === '#' || /^(mailto|tel):/i.test(href)) {
      return false;
    }
    try {
      var url = new URL(link.href, window.location.href);
      return url.origin === window.location.origin;
    } catch (_error) {
      return false;
    }
  }

  function restoreScroll() {
    if (!restorePending || rememberedScrollTop === null) {
      return;
    }
    var expected = rememberedScrollTop;
    var apply = function () {
      var scrollwrap = getScrollwrap();
      if (scrollwrap) {
        scrollwrap.scrollTop = expected;
      }
    };

    window.requestAnimationFrame(function () {
      apply();
      window.requestAnimationFrame(function () {
        apply();
        restorePending = false;
      });
    });
  }

  document.addEventListener('click', function (event) {
    var target = event.target;
    if (!(target instanceof Element)) {
      return;
    }
    var link = target.closest('a[href]');
    if (!isInternalLink(link)) {
      return;
    }
    rememberScroll();
    restorePending = true;
  }, true);

  watchSidebar();
  if (window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(function () {
      watchSidebar();
      restoreScroll();
    });
  }
})();
"""


def write_all():
    PAGES.clear()
    sync_marketing_images()
    ensure_icon_assets(FETCH_ICONS, USE_VISUAL_PACK_ICONS)
    basic_pages()
    getting_started_pages()
    player_pages()
    station_pages()
    recipes_pages()
    gardening_pages()
    food_system_pages()
    server_owner_pages()
    customization_pages()
    addons_pages()
    reference_pages()
    legacy_path_pages()

    docs_dir = DOCS_ROOT / "docs"
    for path, content in PAGES.items():
        target = docs_dir / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    (DOCS_ROOT / "mkdocs.yml").write_text(build_nav(), encoding="utf-8")
    (docs_dir / "stylesheets").mkdir(parents=True, exist_ok=True)
    (docs_dir / "stylesheets/extra.css").write_text(css(), encoding="utf-8")
    (docs_dir / "javascripts").mkdir(parents=True, exist_ok=True)
    (docs_dir / "javascripts/navigation-scroll.js").write_text(navigation_scroll_js(), encoding="utf-8")
    (DOCS_ROOT / "tools").mkdir(parents=True, exist_ok=True)
    (DOCS_ROOT / "tools/generate_reference_pages.py").write_text(helper_script(), encoding="utf-8")

    keep = {str(Path(path)) for path in PAGES}
    for md in docs_dir.rglob("*.md"):
        rel = str(md.relative_to(docs_dir))
        if rel not in keep:
            md.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Regenerate the Heirloom MkDocs wiki from source JSON resources.")
    parser.add_argument("--fetch-icons", action="store_true", help="Download and cache missing player-head and vanilla item icons.")
    parser.add_argument("--use-visual-pack-icons", action="store_true", help="Prefer bundled Nexo/ItemsAdder visual-pack PNGs for wiki item icons. By default, player-head items use generated isometric icons and vanilla items use Minecraft textures.")
    args = parser.parse_args()
    FETCH_ICONS = args.fetch_icons
    USE_VISUAL_PACK_ICONS = args.use_visual_pack_icons
    write_all()
    missing_count = len([entry for entry in ICON_MANIFEST.values() if entry.get("status") != "ok"])
    print(f"Wrote {len(PAGES)} wiki pages to {DOCS_ROOT / 'docs'}")
    print(f"Icon manifest: {len(ICON_MANIFEST)} entries, {missing_count} missing")

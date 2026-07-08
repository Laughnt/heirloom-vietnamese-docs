#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOILING_POT = ROOT / "docs/recipes/station-boiling-pot.md"
DEFAULT_RECIPES = ROOT / "docs/recipes/default-recipes.md"
CSS = ROOT / "docs/stylesheets/extra.css"


def assert_contains(text: str, needle: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing expected text: {needle}")


def assert_not_contains(text: str, needle: str) -> None:
    if needle in text:
        raise AssertionError(f"Unexpected text present: {needle}")


def main() -> int:
    station = BOILING_POT.read_text(encoding="utf-8")
    details = DEFAULT_RECIPES.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    combined = station + "\n" + details

    assert_not_contains(combined, "up to")
    assert_not_contains(combined, '<details class="hl-ingredient-slot')
    assert_not_contains(combined, 'hl-slot-summary')
    assert_not_contains(combined, 'hl-slot-choice-count')
    assert_not_contains(combined, '<span class="hl-slot-count">1</span>')
    assert_not_contains(combined, '<span class="hl-slot-count">1x</span>')
    assert_contains(station, 'title="Required slot 1: 2; POTATO"><span class="hl-slot-box">')
    assert_contains(station, '<span class="hl-slot-count">2</span></span></span>')
    assert_contains(station, '<span class="hl-slot-count">1-3</span></span></span>')
    assert_contains(station, '<span class="hl-slot-count">0-1</span></span></span>')
    assert_contains(station, '<span class="hl-choice-separator">or</span>')
    assert_contains(station, 'title="Required slot 1: 1; COD or SALMON"><span class="hl-slot-box"><span class="hl-slot-choice-icons"')

    assert_contains(css, '.md-typeset .hl-slot-box')
    assert_contains(css, '.md-typeset .hl-recipe-slots .hl-item-icon')
    assert_contains(css, 'width: 48px;')
    assert_contains(css, 'height: 48px;')
    assert_contains(css, 'border: 0;')
    assert_contains(css, '.md-typeset .hl-output-item .hl-item-icon')
    assert_not_contains(css, '.md-typeset .hl-slot-summary')
    assert_not_contains(css, '.md-typeset .hl-slot-choice-count')
    assert_not_contains(css, '.md-typeset .hl-slot-range')
    assert_not_contains(css, 'details.hl-ingredient-slot')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

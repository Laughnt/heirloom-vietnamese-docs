# Plant Types

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

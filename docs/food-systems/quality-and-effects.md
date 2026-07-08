# Quality And Effects

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

# Region Protection

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

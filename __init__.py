from __future__ import annotations

import math
from typing import Any

import unrealsdk
from mods_base import Game, Mod, SliderOption, build_mod, hook
from unrealsdk import logging
from unrealsdk.hooks import Type
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct

assert Game.get_current() is Game.BL3, "Faster Longbow supports Borderlands 3 only"

LONG_BOW_PART = (
    "/Game/Gear/GrenadeMods/_Design/PartSets/Part_Manufacturer/"
    "GM_Part_Manufacturer_03_Hyperion.GM_Part_Manufacturer_03_Hyperion"
)

TARGET_ASSETS = {
    "/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Skills/CharacterSkills/3rd/"
    "AS_UA_Grenade.AS_UA_Grenade",
    "/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Skills/CharacterSkills/3rd/"
    "AS_Grenade_Offhand.AS_Grenade_Offhand",
    "/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Skills/CharacterSkills/3rd/"
    "AS_Grenade_Crouch.AS_Grenade_Crouch",
    "/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Skills/CharacterSkills/3rd/"
    "AS_Grenade.AS_Grenade",
}

# Hard safety limits.  The UI sliders use the same limits, and runtime reads
# are validated again in case the settings JSON is edited manually.
RATE_MIN = 1.0
RATE_MAX = 5.0
LONG_DELAY_MIN = 0.11
LONG_DELAY_MAX = 0.50
DIVIDER_DELAY_MIN = 0.05
DIVIDER_DELAY_MAX = 0.60

throw_rate_option = SliderOption(
    "throw_rate_scale",
    2.5,
    RATE_MIN,
    RATE_MAX,
    0.1,
    is_integer=False,
    display_name="Throw Animation RateScale",
    description=(
        "Speed multiplier for the Longbow grenade throw animation. "
        "Stock is 1.0. Default: 2.5. Safe range: 1.0-5.0."
    ),
)

longbow_delay_option = SliderOption(
    "longbow_teleport_delay",
    0.11,
    LONG_DELAY_MIN,
    LONG_DELAY_MAX,
    0.01,
    is_integer=False,
    display_name="Longbow Teleport Delay",
    description=(
        "Delay before a normal Longbow begins its teleport. "
        "BL3 stock is 0.30 s. Default: 0.11 s. Safe range: 0.11-0.50 s."
    ),
)

divider_delay_option = SliderOption(
    "divider_longbow_teleport_delay",
    0.20,
    DIVIDER_DELAY_MIN,
    DIVIDER_DELAY_MAX,
    0.01,
    is_integer=False,
    display_name="Divider Longbow Teleport Delay",
    description=(
        "Longbow delay used by Divider-style behavior. "
        "BL3 stock is 0.40 s. Default: 0.20 s. Safe range: 0.05-0.60 s."
    ),
)

OPTIONS = (
    throw_rate_option,
    longbow_delay_option,
    divider_delay_option,
)

_anim_assets: list[tuple[UObject, float]] = []
_anim_cache_ready = False

_patch_owner: UObject | None = None
_patch_active = False

_delivery_obj: UObject | None = None
_delivery_old: tuple[float, float] | None = None


def _error(msg: str) -> None:
    logging.error(f"[Faster Longbow] {msg}")


def _path(obj: Any) -> str:
    if obj is None:
        return "<None>"
    try:
        return str(obj._path_name())
    except Exception:
        return "<unreadable-path>"


def _class_name(obj: Any) -> str:
    if obj is None:
        return "<None>"
    try:
        return str(obj.Class.Name)
    except Exception:
        return type(obj).__name__


def _validated(
    raw: Any,
    default: float,
    minimum: float,
    maximum: float,
    label: str,
) -> float:
    try:
        value = float(raw)
    except (TypeError, ValueError):
        _error(f"{label}: invalid value {raw!r}; using default {default:.3f}")
        return default

    if not math.isfinite(value):
        _error(f"{label}: non-finite value {value!r}; using default {default:.3f}")
        return default

    if value < minimum:
        _error(f"{label}: {value:.3f} below safe minimum; clamped to {minimum:.3f}")
        return minimum

    if value > maximum:
        _error(f"{label}: {value:.3f} above safe maximum; clamped to {maximum:.3f}")
        return maximum

    return value


def _current_values() -> tuple[float, float, float]:
    rate = _validated(
        throw_rate_option.value,
        2.5,
        RATE_MIN,
        RATE_MAX,
        "Throw Animation RateScale",
    )
    long_delay = _validated(
        longbow_delay_option.value,
        0.11,
        LONG_DELAY_MIN,
        LONG_DELAY_MAX,
        "Longbow Teleport Delay",
    )
    divider_delay = _validated(
        divider_delay_option.value,
        0.20,
        DIVIDER_DELAY_MIN,
        DIVIDER_DELAY_MAX,
        "Divider Longbow Teleport Delay",
    )
    return rate, long_delay, divider_delay


def _sanitize_loaded_settings(mod: Mod) -> None:
    corrected = False

    specs = (
        (
            throw_rate_option,
            2.5,
            RATE_MIN,
            RATE_MAX,
            "Throw Animation RateScale",
        ),
        (
            longbow_delay_option,
            0.11,
            LONG_DELAY_MIN,
            LONG_DELAY_MAX,
            "Longbow Teleport Delay",
        ),
        (
            divider_delay_option,
            0.20,
            DIVIDER_DELAY_MIN,
            DIVIDER_DELAY_MAX,
            "Divider Longbow Teleport Delay",
        ),
    )

    for option, default, minimum, maximum, label in specs:
        safe = _validated(option.value, default, minimum, maximum, label)
        try:
            current = float(option.value)
        except (TypeError, ValueError):
            current = float("nan")

        if not math.isfinite(current) or current != safe:
            option.value = safe
            corrected = True

    if corrected:
        try:
            mod.save_settings()
        except Exception as exc:
            _error(f"could not persist corrected settings: {exc}")


def _find_equipped_longbow(player: UObject) -> UObject | None:
    try:
        slots = player.EquippedInventory.InventorySlots
    except Exception:
        return None

    for slot in slots:
        try:
            item = slot.EquippedInventory
        except Exception:
            continue
        if item is None:
            continue

        try:
            state = item.BalanceStateComponent
            if state is None:
                continue
            parts = state.GetPartList()
        except Exception:
            continue

        for part in parts:
            if part is None:
                continue
            try:
                if part._path_name() == LONG_BOW_PART:
                    return item
            except Exception:
                continue

    return None


def _get_longbow_delivery(grenade_mod: UObject) -> UObject | None:
    try:
        delivery = grenade_mod.GrenadeDelivery
    except Exception:
        return None

    if delivery is None:
        return None

    if "longbow" not in f"{_class_name(delivery)} {_path(delivery)}".lower():
        return None

    return delivery


def _cache_anim_assets() -> bool:
    global _anim_cache_ready, _anim_assets

    if _anim_cache_ready and _anim_assets:
        return True

    found: list[tuple[UObject, float]] = []

    try:
        loaded = list(unrealsdk.find_all("AnimSequenceBase", exact=False))
    except Exception as exc:
        _error(f"animation scan failed: {exc}")
        return False

    for asset in loaded:
        if _path(asset) not in TARGET_ASSETS:
            continue

        try:
            original = float(asset.RateScale)
        except Exception:
            continue

        found.append((asset, original))

    if not found:
        return False

    _anim_assets = found
    _anim_cache_ready = True
    return True


def _restore_owned_patch(reason: str, owner: UObject | None = None) -> None:
    global _patch_owner, _patch_active
    global _delivery_obj, _delivery_old

    if not _patch_active:
        return

    if owner is not None and _patch_owner is not owner:
        return

    for asset, original in _anim_assets:
        try:
            asset.RateScale = original
        except Exception:
            pass

    if _delivery_obj is not None and _delivery_old is not None:
        old_long, old_divider = _delivery_old
        try:
            _delivery_obj.LongbowTeleportDelay = old_long
            _delivery_obj.DividerLongbowTeleportDelay = old_divider
        except Exception:
            pass

    _patch_owner = None
    _patch_active = False
    _delivery_obj = None
    _delivery_old = None


def _apply_for_action(owner: UObject, grenade_mod: UObject) -> None:
    global _patch_owner, _patch_active
    global _delivery_obj, _delivery_old

    _restore_owned_patch("new action safety")

    rate, long_delay, divider_delay = _current_values()

    anim_changed = False
    if _cache_anim_assets():
        for asset, _original in _anim_assets:
            try:
                asset.RateScale = rate
                anim_changed = True
            except Exception:
                pass
    else:
        _error(
            "grenade animation assets were not available at OnBegin; "
            "delivery settings still applied for this throw"
        )

    delivery_changed = False
    delivery = _get_longbow_delivery(grenade_mod)
    if delivery is not None:
        try:
            old_long = float(delivery.LongbowTeleportDelay)
            old_divider = float(delivery.DividerLongbowTeleportDelay)

            _delivery_obj = delivery
            _delivery_old = (old_long, old_divider)

            delivery.LongbowTeleportDelay = long_delay
            delivery.DividerLongbowTeleportDelay = divider_delay
            delivery_changed = True
        except Exception as exc:
            _error(f"delivery patch failed: {exc}")

    if anim_changed or delivery_changed:
        _patch_owner = owner
        _patch_active = True


def _on_disable() -> None:
    _restore_owned_patch("mod disable")


@hook(
    "/Game/PlayerCharacters/_Shared/_Design/GrenadeThrow/"
    "Action_GrenadeThrow_Base.Action_GrenadeThrow_Base_C:OnBegin",
    Type.PRE,
)
def _action_begin(
    obj: UObject,
    args: WrappedStruct,
    _ret: Any,
    _func: BoundFunction,
) -> None:
    try:
        player = args.Actor
    except Exception:
        return

    grenade_mod = _find_equipped_longbow(player)
    if grenade_mod is None:
        return

    _apply_for_action(obj, grenade_mod)


@hook(
    "/Game/PlayerCharacters/_Shared/_Design/GrenadeThrow/"
    "Action_GrenadeThrow_Base.Action_GrenadeThrow_Base_C:OnEnd",
    Type.POST,
)
def _action_end(
    obj: UObject,
    _args: WrappedStruct,
    _ret: Any,
    _func: BoundFunction,
) -> None:
    if _patch_owner is obj:
        _restore_owned_patch("owning Action OnEnd", owner=obj)


# Try to cache eagerly; OnBegin retries if the character assets are not loaded yet.
_cache_anim_assets()

mod = build_mod(
    options=OPTIONS,
    on_disable=_on_disable,
)

# build_mod() loads persisted settings before returning. Sanitize those values,
# including hand-edited JSON, before any gameplay use.
_sanitize_loaded_settings(mod)

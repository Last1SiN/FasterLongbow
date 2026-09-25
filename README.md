# FasterLongbow

[English](README.md) | [Русский](README_RU.md)

FasterLongbow makes Longbow grenades feel less sluggish.

The grenade leaves your hand faster and teleports sooner, while every other grenade delivery type is left alone. The default timings are tuned to feel quicker without breaking the teleport, and you can adjust them from the Mod Menu if you want.

## Features

- Faster Longbow throw animation.
- Shorter delay before the grenade teleports.
- Separate timing for Divider-style Longbow grenades.
- All three values can be adjusted in the Mod Menu.
- Only affects Longbow delivery; other grenade types are untouched.
- Keeps unsafe timing values from breaking the teleport.
- Restores temporary animation changes after the throw is finished.

## Configuration

Default values are the tested release settings:

- **Throw Animation RateScale:** `2.5`
- **Longbow Teleport Delay:** `0.11 s`
- **Divider Longbow Teleport Delay:** `0.20 s`

Allowed ranges:

- **Throw Animation RateScale:** `1.0-5.0`
- **Longbow Teleport Delay:** `0.11-0.50 s`
- **Divider Longbow Teleport Delay:** `0.05-0.60 s`

`Longbow Teleport Delay` is hard-limited to **0.11 s minimum**. Testing showed that lower values can break Longbow teleport behavior.

The current throw-animation acceleration targets the tested **FL4K / Beastmaster** grenade animation assets. Longbow delivery timing itself is not limited to those animation assets.

## Requirements

- Borderlands 3
- [BL3 PythonSDK / Oak Mod Manager](https://github.com/bl-sdk/oak-mod-manager/releases/latest)

Use the [official BL3 SDK / Oak installation guide](https://bl-sdk.github.io/oak-mod-db/) for SDK installation and updates.

## Installing the mod

1. Install or update BL3 PythonSDK / Oak using the official guide above.
2. Download `FasterLongbow.sdkmod` from [GitHub Releases](https://github.com/Last1SiN/FasterLongbow/releases/latest).
3. With Borderlands 3 closed, copy the `.sdkmod` file intact to `Borderlands 3\sdk_mods\`. Do not extract the `.sdkmod` itself.
4. Start the game, open **MODS -> FasterLongbow**, enable the mod and configure it under **Options**.

To update FasterLongbow, replace the existing `.sdkmod` with the newer file and restart the game.

## Compatibility and license

- Co-op support: **Unknown** — behavior with the mod installed only on a client while the host does not have it has not yet been validated.
- Other grenade delivery types are not intentionally modified.
- License: **GNU GPLv3 with [Section 7 additional provenance terms](ADDITIONAL_TERMS.md)**

## Credits

**Development:** Sol / GPT-5.6 Sol  
**Design, testing & QA:** Last1SiN

**BL3 PythonSDK / Oak Mod Manager:** created by [apple1417](https://github.com/apple1417), with contributions from the [BL-SDK](https://github.com/bl-sdk) project and contributors.

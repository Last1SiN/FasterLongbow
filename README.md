# FasterLongbow

FasterLongbow makes Longbow grenades feel faster and more responsive by accelerating the grenade throw animation and shortening the pre-teleport delay, without changing other grenade delivery types.

## Features

- Applies only when the equipped grenade uses Longbow delivery.
- Accelerates the tested Longbow grenade throw animation.
- Shortens the Longbow pre-teleport delay.
- Exposes all three timing values in the Mod Menu.
- Validates custom values before applying them.
- Restores temporary runtime changes when the owning grenade action ends.
- Does not edit the `SpawnAndThrowGrenade` notify.
- Does not use action `PlayRate`, `OverridePlayRate`, or CDO timing hacks.
- No normal gameplay log spam; the mod writes only errors.

## Configuration

Default values are the tested release settings:

- **Throw Animation RateScale:** `2.5`
- **Longbow Teleport Delay:** `0.11 s`
- **Divider Longbow Teleport Delay:** `0.20 s`

Allowed ranges:

- **Throw Animation RateScale:** `1.0-5.0`
- **Longbow Teleport Delay:** `0.11-0.50 s`
- **Divider Longbow Teleport Delay:** `0.05-0.60 s`

`Longbow Teleport Delay` is hard-limited to **0.11 s minimum**. Testing showed that lower values can break Longbow teleport behavior. The Mod Menu slider and runtime validation both enforce the same minimum, including values injected through a manually edited settings file.

The current throw-animation RateScale implementation targets the tested **FL4K / Beastmaster** grenade animation assets.

## Requirements

- Borderlands 3.
- [BL3 PythonSDK / Oak Mod Manager v1.11+ — latest stable release](https://github.com/bl-sdk/oak-mod-manager/releases/latest).
- [Official BL3 SDK installation guide](https://bl-sdk.github.io/oak-mod-db/).

Oak Mod Manager v1.11 bundles the required **Mods Base 1.12**, **BL3 Mod Menu 1.8**, **pyunrealsdk 1.10.0**, and **unrealsdk 3.2.0** components. They do not need to be downloaded separately when using that release or a newer compatible Oak release.

## Installation

1. **Fully close Borderlands 3.**
2. If BL3 PythonSDK / Oak is not installed, or you want to update it, open the [latest stable Oak Mod Manager release](https://github.com/bl-sdk/oak-mod-manager/releases/latest). Under **Assets**, download **`bl3-sdk.zip`** — not either `Source code` archive.
3. Locate the Borderlands 3 game folder. In Steam: **Library -> right-click Borderlands 3 -> Manage -> Browse local files**. Extract the contents of `bl3-sdk.zip` directly into the **Borderlands 3 game folder**, allowing folders/files to merge and accepting overwrite prompts. For the complete procedure, including Proton/Linux notes, use the [official BL3 SDK installation guide](https://bl-sdk.github.io/oak-mod-db/).
4. Start Borderlands 3 once after installing/updating the SDK and verify that a new **MODS** entry appears on the main menu.
5. Download the latest **FasterLongbow** from [GitHub Releases](https://github.com/Last1SiN/FasterLongbow/releases/latest).
6. Fully close the game again and copy `FasterLongbow.sdkmod` **without extracting it** to:

   `Borderlands 3\sdk_mods\`

7. Start/restart Borderlands 3, open **MODS -> FasterLongbow**, enable the mod, and open **Options** to configure the timing values.

To update FasterLongbow, replace the existing `FasterLongbow.sdkmod` with the newer file and restart the game.

Remove old FasterLongbow test/probe builds or extracted FasterLongbow folders before installing the release so that only one copy of the mod can load.

## Compatibility and license

- Co-op support: **Unknown** — not yet validated.
- Character scope: Longbow delivery timing is general, while the current throw-animation acceleration targets the tested **FL4K / Beastmaster** grenade animation assets.
- License: **GPL-3.0**

## Credits

- **Mod creator / code:** Sol (ChatGPT, GPT-5.6 Sol)
- **QA / maintainer:** [Last1SiN](https://github.com/Last1SiN)
- **BL3 PythonSDK / Oak Mod Manager:** created by [apple1417](https://github.com/apple1417), with contributions from the [BL-SDK](https://github.com/bl-sdk) project and contributors.

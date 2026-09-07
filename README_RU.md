# FasterLongbow

[English](README.md) | [Русский](README_RU.md)

FasterLongbow делает Longbow-гранаты в Borderlands 3 быстрее и отзывчивее: ускоряет анимацию броска и сокращает паузу перед телепортацией, не изменяя другие типы доставки гранат.

## Возможности

- Работает только когда экипированная граната использует Longbow delivery.
- Ускоряет протестированную анимацию броска Longbow-гранаты.
- Сокращает паузу перед Longbow-телепортацией.
- Имеет отдельный параметр тайминга для Divider-style Longbow behavior.
- Выводит все три параметра в Mod Menu.
- Проверяет пользовательские и вручную отредактированные значения перед применением.
- Восстанавливает временные runtime-изменения после завершения конкретного grenade action.
- Не изменяет другие типы доставки гранат.
- При обычной работе пишет в лог только ошибки.

## Настройка

Протестированные значения по умолчанию:

- **Throw Animation RateScale:** `2.5`
- **Longbow Teleport Delay:** `0.11 с`
- **Divider Longbow Teleport Delay:** `0.20 с`

Допустимые диапазоны:

- **Throw Animation RateScale:** `1.0-5.0`
- **Longbow Teleport Delay:** `0.11-0.50 с`
- **Divider Longbow Teleport Delay:** `0.05-0.60 с`

`Longbow Teleport Delay` жёстко ограничен минимумом **0.11 с**. В тестах меньшие значения могли ломать Longbow-телепортацию.

Текущее ускорение throw-animation использует протестированные animation assets **FL4K / Beastmaster**. Сам тайминг Longbow delivery этими assets не ограничен.

## Требования

- Borderlands 3
- [BL3 PythonSDK / Oak Mod Manager](https://github.com/bl-sdk/oak-mod-manager/releases/latest)

Для установки и обновления SDK используйте [официальную инструкцию BL3 SDK / Oak](https://bl-sdk.github.io/oak-mod-db/).

## Установка мода

1. Установите или обновите BL3 PythonSDK / Oak по официальной инструкции выше.
2. Скачайте `FasterLongbow.sdkmod` из [GitHub Releases](https://github.com/Last1SiN/FasterLongbow/releases/latest).
3. При полностью закрытой Borderlands 3 скопируйте `.sdkmod` целиком в `Borderlands 3\sdk_mods\`. Сам `.sdkmod` распаковывать не нужно.
4. Запустите игру, откройте **MODS -> FasterLongbow**, включите мод и настройте его через **Options**.

Для обновления замените существующий `.sdkmod` новым файлом и перезапустите игру. Удалите старые test/probe-сборки и распакованные копии, чтобы загружался только один экземпляр FasterLongbow.

## Совместимость и лицензия

- Кооператив: **Unknown** — сценарий, где мод установлен только у клиента, а у хоста его нет, пока не проверен.
- Другие типы доставки гранат намеренно не изменяются.
- Лицензия: **GPL-3.0**

## Credits

**Development:** Sol / GPT-5.6 Sol  
**Design, testing & QA:** Last1SiN

**BL3 PythonSDK / Oak Mod Manager:** создан [apple1417](https://github.com/apple1417) при участии проекта и контрибьюторов [BL-SDK](https://github.com/bl-sdk).

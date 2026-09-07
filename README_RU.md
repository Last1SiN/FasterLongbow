# FasterLongbow

**Мод PythonSDK / Oak для Borderlands 3**

Текущий релиз: **v1.1.3**

> Готовые к установке `.sdkmod` публикуются в разделе **Releases**.  
> Файлы в репозитории являются исходниками мода.

---

FasterLongbow делает Longbow-гранаты быстрее и отзывчивее: ускоряет анимацию броска гранаты и сокращает паузу перед телепортацией, не изменяя другие способы доставки гранат.

## Возможности

- Работает только когда экипированная граната использует Longbow delivery.
- Ускоряет протестированную анимацию броска Longbow-гранаты.
- Сокращает паузу перед Longbow-телепортом.
- Выводит все три параметра таймингов в Mod Menu.
- Проверяет пользовательские значения перед применением.
- Восстанавливает временные runtime-изменения после завершения конкретного grenade action.
- Не изменяет `SpawnAndThrowGrenade` notify.
- Не использует action `PlayRate`, `OverridePlayRate` или CDO-хаки таймингов.
- Нет обычного игрового спама в лог; мод пишет только ошибки.

## Настройка

Протестированные значения по умолчанию:

- **Throw Animation RateScale:** `2.5`
- **Longbow Teleport Delay:** `0.11 с`
- **Divider Longbow Teleport Delay:** `0.20 с`

Допустимые диапазоны:

- **Throw Animation RateScale:** `1.0-5.0`
- **Longbow Teleport Delay:** `0.11-0.50 с`
- **Divider Longbow Teleport Delay:** `0.05-0.60 с`

`Longbow Teleport Delay` жёстко ограничен минимумом **0.11 с**. В тестах меньшие значения ломали телепорт Longbow. Один и тот же минимум принудительно проверяется как ползунком Mod Menu, так и runtime-валидацией, включая значения, вручную вписанные в файл настроек.

Текущее ускорение throw-animation через RateScale использует протестированные animation assets **FL4K / Beastmaster**.

## Требования

- Borderlands 3.
- [BL3 PythonSDK / Oak Mod Manager v1.11+ — актуальный стабильный релиз](https://github.com/bl-sdk/oak-mod-manager/releases/latest).
- [Официальная инструкция по установке BL3 SDK](https://bl-sdk.github.io/oak-mod-db/).

Oak Mod Manager v1.11 уже включает необходимые **Mods Base 1.12**, **BL3 Mod Menu 1.8**, **pyunrealsdk 1.10.0** и **unrealsdk 3.2.0**. При использовании этого релиза или более новой совместимой версии Oak отдельно скачивать эти компоненты не нужно.

## Установка

1. **Полностью закройте Borderlands 3.**
2. Если BL3 PythonSDK / Oak ещё не установлен или его нужно обновить, откройте [актуальный стабильный релиз Oak Mod Manager](https://github.com/bl-sdk/oak-mod-manager/releases/latest). В разделе **Assets** скачайте именно **`bl3-sdk.zip`**, а не архивы `Source code`.
3. Найдите корневую папку Borderlands 3. В Steam: **Библиотека -> ПКМ по Borderlands 3 -> Управление -> Просмотреть локальные файлы**. Распакуйте содержимое `bl3-sdk.zip` прямо в **корневую папку Borderlands 3**, согласившись на объединение папок/файлов и замену файлов при запросе. Полная процедура, включая Proton/Linux, находится в [официальной инструкции BL3 SDK](https://bl-sdk.github.io/oak-mod-db/).
4. После установки/обновления SDK один раз запустите Borderlands 3 и убедитесь, что в главном меню появился новый пункт **MODS**.
5. Скачайте актуальный **FasterLongbow** из [GitHub Releases](https://github.com/Last1SiN/FasterLongbow/releases/latest).
6. Снова полностью закройте игру и скопируйте `FasterLongbow.sdkmod` **не распаковывая** в:

   `Borderlands 3\sdk_mods\`

7. Запустите/перезапустите Borderlands 3, откройте **MODS -> FasterLongbow**, включите мод и откройте **Options** для настройки таймингов.

Для обновления FasterLongbow замените существующий `FasterLongbow.sdkmod` новой версией файла и перезапустите игру.

Перед установкой релиза удалите старые тестовые/probe-сборки FasterLongbow и старые распакованные папки FasterLongbow, чтобы одновременно загружалась только одна копия мода.

## Совместимость и лицензия

- Кооператив: **ClientSide** — проверено при установленном FasterLongbow только у локального игрока; другой участник кооп-сессии играл без мода.
- Персонажи: настройка Longbow delivery общая, а текущее ускорение throw-animation использует протестированные assets **FL4K / Beastmaster**.
- Лицензия: **GPL-3.0**

## Credits

- **Development:** Sol / GPT-5.6 Sol
- **Design, testing & QA:** Last1SiN
- **BL3 PythonSDK / Oak Mod Manager:** создан [apple1417](https://github.com/apple1417) при участии проекта и контрибьюторов [BL-SDK](https://github.com/bl-sdk).

# greyhound_bin

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

This custom component integrates Greyhound Bin App API with [Home Assistant][ha], it will add a new local calendar allowing you to monitor your Bin collections for the next 30 days. There are a few extra sensors, e.g. - next collection date, next collection bin type.

**This component will set up the following platforms.**

| Platform   | Description                                      |
| ---------- | ------------------------------------------------ |
| `sensor`   | Displays information from the greyhound_bin API. |
| `calendar` | Shows upcoming bin collection events.            |

![example][exampleimg]

## HACS Installation

This is the recommended way to install.

1. Open [HACS][hacs] in your Home Assistant UI
2. Click on the three dots in the top right corner and select Custom repositories.
3. In the "Add custom repository" field, paste https://github.com/JosyBan/greyhound_bin.
4. Select Integration as the Category.
5. Click ADD
6. Once added, search for "ventaxia" in the HACS Integrations section.
7. Click on the "ventaxia" integration.
8. Click Download and confirm.
9. Restart Home Assistant.
10. In the HA UI, click Settings in the left nav bar, then click "Devices & Services". By default you should be viewing the Integrations tab. Click "+ Add Integration" button at bottom right and then search for "ventaxia".

## Manual Installation

1. Download the integration: Download the latest release from the [Release Page][releases].
2. Unpack the ventaxia_ha folder from the downloaded archive.
3. Copy the entire ventaxia_ha folder into your Home Assistant's custom_components directory. If this directory doesn't exist, you'll need to create it.
4. Your Home Assistant configuration directory typically resides at /config (e.g., /config/custom_components/ventaxia_ha/).
5. Restart Home Assistant.
6. In the HA UI, click Settings in the left nav bar, then click "Devices & Services". By default you should be viewing the Integrations tab. Click "+ Add Integration" button at bottom right and then search for "ventaxia".

## Configuration

After installation and restarting Home Assistant, you can configure the Greyhound Bin integration via the Home Assistant UI.

    Go to Settings > Devices & Services.

    Click on ADD INTEGRATION.

    Search for "Greyhound Bin" and select it.

    Follow the on-screen prompts to enter your Greyhound Bin account details

Once successfully configured, the integration will automatically create the calendar and relevant sensor entities. You can find the full list of available entities under Settings > Devices & Services > Greyhound Bin integration once it's set up.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[buymecoffee]: https://www.buymeacoffee.com/JosyBan
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/JosyBan/greyhound_bin.svg?style=for-the-badge
[commits]: https://github.com/JosyBan/greyhound_bin/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: logo@x2.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/JosyBan/greyhound_bin.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40JosyBan-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/JosyBan/greyhound_bin.svg?style=for-the-badge
[releases]: https://github.com/JosyBan/greyhound_bin/releases
[user_profile]: https://github.com/JosyBan
[greyhound_bin]: https://github.com/JosyBan/greyhound_bin

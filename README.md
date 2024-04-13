# 🤖 TON Token Access Control Bot

[![TON](https://img.shields.io/badge/TON-grey?logo=TON&logoColor=40AEF0)](https://ton.org)
[![Telegram Bot](https://img.shields.io/badge/Bot-grey?logo=telegram)](https://core.telegram.org/bots)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License](https://img.[db](app%2Fdb)shields.io/github/license/nessshon/token-access-control-bot)](https://github.com/nessshon/token-access-control-bot/blob/main/LICENSE)
[![Redis](https://img.shields.io/badge/Redis-Yes?logo=redis&color=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-blue?logo=docker&logoColor=white)](https://www.docker.com/)

...

* Bot example: [@TONTokenAccessControlBot](https://t.me/TONTokenAccessControlBot)

## Features

* **TON-Connect Integration:** For a secure and user-friendly experience.

* **Testnet and Mainnet Support:** Supports testnet and mainnet for flexible testing and deployment.

* **Multilingual Support:** Supports both Russian and English for user interaction.

## Usage

<details>
<summary><b>Preparation</b></summary>

1. Create a private group and/or channel.

2. Create a bot via [@BotFather](https://t.me/BotFather) and save the `TOKEN` (later referred to as `BOT_TOKEN`).

3. Create an API key on [tonconsole.com](https://tonconsole.com) (later referred to as `TONAPI_KEY`).

4. Obtain a key for TON Connect (Optional, later referred to as `TONAPI_TONCONNECT_KEY`). This key is necessary for the
   proper functioning of TON Connect on the backend under heavy user load. You can get the key by contacting @subden via
   private message. Inform him about your project and the need for this key.

5. If desired, customize the bot's texts in
   the [texts](https://github.com/nessshon/token-access-control-bot/blob/main/app/texts.py) file according to your
   requirements.

6. if desired, add your preferred language
   to [SUPPORTED_LANGUAGES](https://github.com/nessshon/token-access-control-bot/blob/main/app/texts.py#L4) and add the
   corresponding codes to [TEXT_BUTTONS](https://github.com/nessshon/token-access-control-bot/blob/main/app/texts.py#L9)
   and [TEXT_MESSAGES](https://github.com/nessshon/token-access-control-bot/blob/main/app/texts.py#L54).

7. Clone the repository:

    ```bash
    git clone https://github.com/nessshon/token-access-control-bot.git
    ```

8. Navigate to the bot directory:

    ```bash
    cd token-access-control-bot
    ```

9. Clone the environment variables file:

   ```bash
   cp .env.example .env
   ```

10. Configure [environment variables](#environment-variables-reference) variables file:

    ```bash
    nano .env
    ```

11. Install Docker and Docker Compose:

    ```bash
    sudo apt install docker.io && docker-compose -y
    ```

12. Run the bot in a Docker container:

    ```bash
    docker-compose up --build
    ```

13. Start the bot with the command `/start`, choose the language, and authenticate using TON Connect.

14. Access the admin panel with the command `/admin` and add the token.

15. Add the bot to your private chat, ensuring you grant permissions to add administrators. After that, the bot will
    prompt you to add the chat to the database for monitoring.

16. You're all set!

</details>

## Environment Variables Reference

<details>
<summary>Click to expand</summary>

Here's a comprehensive reference guide for the environment variables used in the project:

| Variable                                  | Type   | Description                                                                                                                                                                                                                   | Example                                                                                   |
|-------------------------------------------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| `BOT_TOKEN`                               | `str`  | Bot token obtained from [@BotFather](https://t.me/BotFather)                                                                                                                                                                  | `123456:qweRTY`                                                                           | 
| `BOT_DEV_ID`                              | `int`  | User ID of the bot developer, obtain it from [my_id_bot](https://t.me/my_id_bot)                                                                                                                                              | `123456789`                                                                               |
| `BOT_ADMIN_ID`                            | `int`  | User ID of the bot admin, obtain it from [my_id_bot](https://t.me/my_id_bot)                                                                                                                                                  | `123456789`                                                                               |
| `IS_TESTNET`                              | `bool` | Set to `True` for TON testnet or `False` for mainnet                                                                                                                                                                          | `False`                                                                                   |
| `MANIFEST_URL`                            | `str`  | URL of the bot's manifest file                                                                                                                                                                                                | `https://github.com/nessshon/token-access-control-bot/blob/main/tonconnect-manifest.json` |
| `TONAPI_KEY`                              | `str`  | API key for TONAPI, obtain it from [tonconsole.com](https://tonconsole.com)                                                                                                                                                   | `AE33E...3FYQ`                                                                            |
| `TONAPI_TONCONNECT_KEY`                   | `str`  | API key for TON Connect (optional), obtain it by contacting [@subden](https://t.me/subden)                                                                                                                                    | `587d4...5a71`                                                                            |
| `SCHEDULER_CHECK_CHAT_MEMBERS_INTERVAL`   | `int`  | Interval (minutes) for checking chat members (1-5 minutes is acceptable)                                                                                                                                                      | `587d4...5a71`                                                                            |
| `SCHEDULER_UPDATE_TOKEN_HOLDERS_INTERVAL` | `int`  | Interval (minutes) for updating token holders (adjust value by Jetton holders or NFT elements. Every 1000 tokens or holders equals 1-2 seconds. For instance, for collections with 30k or fewer elements, set the value to 1) | `587d4...5a71`                                                                            |
| `REDIS_HOST`                              | `str`  | Hostname or IP address of the Redis server (set `redis` if you don't have your own Redis server)                                                                                                                              | `redis`                                                                                   |
| `REDIS_PORT`                              | `int`  | Port number of the Redis server (set `6379` if you don't have your own Redis server)                                                                                                                                          | `6379`                                                                                    |
| `REDIS_DB`                                | `int`  | Redis database number (set `0` if you don't have your own Redis server)                                                                                                                                                       | `0`                                                                                       |

</details>

## Contribution

We welcome your contributions! If you have ideas for improvement or have identified a bug, please create an issue or
submit a pull request.

## Support

Supported by [TON Society](https://github.com/ton-society/grants-and-bounties), Grants and Bounties program.

## License

This repository is distributed under
the [MIT License](https://github.com/nessshon/token-access-control-bot/blob/main/LICENSE).

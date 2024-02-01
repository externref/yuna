# yuna

## Setup

Create `.env` file with the bot token and postgresql URL in this format
```
TOKEN="TOKEN HERE"
PGSQL_URL="URL HERE"
```

## Running the bot

```sh
python -m pip install poetry
python -m poetry install
python -m poetry shell
python -m yuna start
```
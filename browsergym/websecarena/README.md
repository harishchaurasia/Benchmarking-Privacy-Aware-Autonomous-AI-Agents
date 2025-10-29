# WebSecArena benchmark for BrowserGym

This package provides `browsergym.websecarena`, which is an official port of the [WebSecArena](https://github.com/harishchaurasia/Benchmarking-Privacy-Aware-Autonomous-AI-Agents) benchmark for BrowserGym.

## Setup (Currently not needed)

### Option 1: Automated setup (Recommended)

If you're working from the BrowserGym root directory, you can use the Makefile for automated setup:

```sh
make setup-websecarena
```

This will:

- Clone the WebSecArea repository
- Add the `WEBSECARENA_URL` to your `.env` file

Then load the environment variables:

```sh
source .env
```

### Option 2: Manual setup

1. Clone WebSecArena

```sh
git clone <WebSecArena Repo URL>
```

2. Setup WebSecArena URL (change `PATH_TO_WEBSECARENA_CLONED_REPO` here to the absolute path to your `websecarena` folder)

```sh
export MINIWOB_URL="file://<PATH_TO_WEBSECARENA_CLONED_REPO>/websecarena/html/websecarena/"
```
# Discord Vanity URL Sniper

## Description

This project is an asynchronous Discord vanity URL sniper written in Python. It utilizes the `aiohttp` library to perform HTTP requests asynchronously, allowing for efficient testing of Discord vanity URLs. The code includes functions for claiming vanities, fetching vanities, and executing threads. It also incorporates error handling and notification capabilities through webhooks.

Please note that this project is intended for educational purposes only and should be used responsibly and within the bounds of legal and ethical considerations.

## Features

- Asynchronous HTTP requests using `aiohttp`
- Vanity URL claiming functionality
- Error handling and notification system
- Multi-threaded execution for efficient testing
- Customizable delay between requests

## Installation

1. Clone the repository:

```git clone https://github.com/your-username/discord-vanity-sniper.git```

2. Install the required dependencies:

```pip install -r requirements.txt```

## Configuration

Before running the sniper, make sure to configure the following variables in the `sniper.py` file:

- `TOKEN`: Your Discord bot token
- `WEBHOOK_URL`: The URL of the webhook to send notifications
- `GUILD_ID`: The ID of the Discord server where the vanity URLs will be claimed
- `VANITY_LIST`: A list of vanity URLs to test
- `DELAY`: The delay in seconds between each request

## Usage

Run the `sniper.py` file to start the sniper:

```py sniper.py```

The sniper will continuously test the specified vanity URLs and attempt to claim them if available. Notifications will be sent to the configured webhook URL upon successful or failed claims.

## Disclaimer

This project is for educational purposes only. Use it responsibly and at your own risk. The developers are not responsible for any misuse or violation of Discord's terms of service.

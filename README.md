# urcl-poll-bot
Polling bot for the URCL Discord server.

## Usage

This bot will only process messages in the channel named by the POLL_CHANNEL constant (located in main.py). It expects that a valid Discord user token exists as the environment variable TOKEN, which can be set with `$ export TOKEN="..."`. To start a poll, send a message in the polls channel with the following format:

```
!poll
time [number of hours]
desc [poll description]
opt [first option]
opt [second option]
...
```

Notes:
- The `time` parameter is optional, and defaults to 24 if not provided. It is always an integer number of hours.
- Each `desc` line will be formatted as one paragraph of the poll's description. There must be at least one.
- Each `opt` parameter is one option to be voted on. Each is assigned to a letter. There must be at least two and at most 26 options.

After processing this message, the bot will send a poll message with an @here ping listing the options. It will react to this message with each letter option, so that the reactions can be used for voting. After the specified number of hours, the bot will reply to this message with a tally of the poll results at that moment.

This bot is able to conduct multiple ongoing polls simultaneously. A poll can be cancelled simply by deleting the bot's polling message.

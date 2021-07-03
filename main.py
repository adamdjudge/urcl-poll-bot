#!/usr/bin/env python3

import discord
import asyncio
import os

# Default poll duration in hours.
DEFAULT_DURATION = 24

# Name of polls channel. Commands aren't processed in any other channel.
POLL_CHANNEL = "urcl-polls"

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Initialized as", client.user)

@client.event
async def on_message(msg):
    if msg.author == client.user or str(msg.channel) != POLL_CHANNEL:
        return

    if msg.content.startswith("!poll"):
        lines = msg.content.splitlines()
        ch = msg.channel
        time = DEFAULT_DURATION
        desc = []
        opts = []
        for line in lines[1:]:
            if len(line.split()) < 2:
                await ch.send(f"{line} parameter missing value.")
                return
            
            key, val = line.split(' ', 1)
            if key == "time":
                try:
                    time = int(val)
                except:
                    await ch.send("Invalid time argument.")
                    return
            elif key == "desc":
                desc.append(val)
            elif key == "opt":
                opts.append(val)
            else:
                await ch.send(f"Unknown parameter {key}.")
                return
        
        if len(desc) == 0 or len(opts) < 2:
            await ch.send(
                "Missing parameters. Description and at least two options " +
                "are required."
            )
            return
        
        if len(opts) > 26:
            # Options assigned to letters, so 26 max.
            await ch.send("Too many options (>26).")
            return
        
        text = "@here " + "\n\n".join(desc)
        
        letter = ord('A')
        for opt in opts:
            text += f"\n\n{chr(letter)}) {opt}"
            letter += 1
        
        text += "\n\nPlease vote only once (that includes alt accounts). " \
            + f"This poll ends {time} hours after it has first been posted."
        
        if len(text) > 2000:
            # Discord message length limit is 2000 chars.
            await ch.send("Poll message too long (>2000 chars).")
            return
        
        pollmsg = await ch.send(text)
        valid_reacts = []
        for i in range(len(opts)):
            emoji = chr(ord('🇦') + i)
            valid_reacts.append(emoji)
            await pollmsg.add_reaction(emoji)
        
        # Convert time to hours and wait.
        await asyncio.sleep(time * 3600)

        # Fetch updated message to get current react counts.
        try:
            pollmsg = await ch.fetch_message(pollmsg.id)
        except:
            # Deleting the message simply cancels the poll.
            return
        
        text = "This poll has ended! Final results:"
        for react in pollmsg.reactions:
            if str(react) in valid_reacts:
                text += f"\n{str(react)} - {react.count-1}"
        await pollmsg.reply(text)

if __name__ == "__main__":
    client.run(os.environ["TOKEN"])

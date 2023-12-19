import discord
from discord.ext import commands
import os
from flask import Flask, request
import threading
import sys
import asyncio
from ddns import ddns_service
from server import start_minecraft_server
from globals import DISCORD_TOKEN, MINECRAFT_CHANNEL_ID

bot = discord.Bot()
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", help_command=None, intents=intents)

app = Flask(__name__)

async def run_bot():
    await bot.start(DISCORD_TOKEN)

def run_flask():
    app.run(host="0.0.0.0", port=5000)

async def send_message_with_timeout(channel, content, timeout):
    try:
        await asyncio.wait_for(channel.send(content), timeout=timeout)
        return True
    except asyncio.TimeoutError:
        return False

async def send_embed_with_timeout(channel, embed, timeout):
    try:
        await asyncio.wait_for(channel.send(embed=embed), timeout=timeout)
        return True
    except asyncio.TimeoutError:
        return False


@app.route("/discord_bot", methods=["POST"])
def receive_message():
    # Get message content
    event = request.json.get("event")
    player = request.json.get("player")
    content = request.json.get("content")
    channel = bot.get_channel(MINECRAFT_CHANNEL_ID)
    if event:
        if event == "playerJoin":
            msg = f"**{player}** joined the game!"
            embed = discord.Embed(description=msg, color=discord.Color.green())
            future = asyncio.run_coroutine_threadsafe(
                send_embed_with_timeout(channel, embed, 5), loop
            )
            return "Message sent to Discord channel!"
        elif event == "playerLeft":
            msg = f"**{player}** left the game!"
            embed = discord.Embed(description=msg, color=discord.Color.yellow())
            future = asyncio.run_coroutine_threadsafe(
                send_embed_with_timeout(channel, embed, 5), loop
            )
            return "Message sent to Discord channel!"
        elif event == "playerDeath":
            msg = f"**What a noob! {player} is dead**"
            embed = discord.Embed(description=msg, color=discord.Color.red())
            future = asyncio.run_coroutine_threadsafe(
                send_embed_with_timeout(channel, embed, 5), loop
            )
            return "Message sent to Discord channel!"
        elif event == "playerChat":
            msg = f"{player}: {content}"
            future = asyncio.run_coroutine_threadsafe(
                send_message_with_timeout(channel, msg, 5), loop
            )
            return "Message sent to Discord channel!"
        elif event == "serverStart":
            msg = f"**Server has started !!**"
            embed = discord.Embed(description=msg, color=discord.Color.blue())
            future = asyncio.run_coroutine_threadsafe(
                send_embed_with_timeout(channel, embed, 5), loop
            )
            return "Message sent to Discord channel!"
        elif event == "serverStop":
            msg = f"**Server has stopped !!**"
            embed = discord.Embed(description=msg, color=discord.Color.blue())
            future = asyncio.run_coroutine_threadsafe(
                send_embed_with_timeout(channel, embed, 5), loop
            )
            return "Message sent to Discord channel!"

        if future.result():
            return "Message sent to Discord channel!"
        else:
            return "Sending message timed out!"
    else:
        return "Invalid request data!"

if __name__ == "__main__":

    if (len(sys.argv)==2 and sys.argv[1]=="-bot"):
        for foldername in os.listdir("./cogs"):
            for filename in os.listdir(f"./cogs/{foldername}"):
                if filename.endswith(".py"):
                    bot.load_extension(f"cogs.{foldername}.{filename[:-3]}")

        ddns_thread = threading.Thread(target=ddns_service)
        ddns_thread.start()

        loop = asyncio.get_event_loop()
        loop.create_task(run_bot())
        threading.Thread(target=run_flask).start()
        loop.run_forever()
    else:
        server_thread = threading.Thread(target=start_minecraft_server)
        server_thread.start()


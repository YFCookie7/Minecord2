import discord
from discord.ext import commands
import json
from globals import MINECRAFT_LOG_CHANNEL_ID, MINECRAFT_CHANNEL_ID
import os
import subprocess
import time
import threading
from flask import Flask, request
import sys
import asyncio
from queue import Queue, Empty


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as {0.user}".format(self.bot))
        print(f"{self.bot.user.name} is now online!")
        channel = self.bot.get_channel(MINECRAFT_CHANNEL_ID)
        bot_enabled = True
        server_thread = threading.Thread(target=self.start_minecraft_server)
        server_thread.start()
        await self.bot.change_presence(activity=discord.Game(name="Minecraft Server"))
        await channel.send("Crafty Cookiebot is ready!")

    
    def read_output(self, queue, process):
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                queue.put(output.strip())

    async def send_accumulated_messages(self, message):
        channel = self.bot.get_channel(MINECRAFT_LOG_CHANNEL_ID)
        await channel.send(message, silent=True)

    def start_minecraft_server(self):
        server_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..'))
        os.chdir(server_directory)
        command = 'java -Xmx16G -Xms16G -jar "server.jar" nogui'

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        output_queue = Queue()

        output_thread = threading.Thread(target=self.read_output, args=(output_queue, process))
        output_thread.start()
        # if (len(sys.argv)==2 and sys.argv[1]=="-bot"):
        accumulated_messages = ""
        output = ""
        start_time = time.time()
        while True:
            try:
                output = output_queue.get_nowait()
                accumulated_messages += (output + "\n")
                # print(output)
            except Empty:
                time.sleep(0.1)
            if (time.time() - start_time >= 15 or len(accumulated_messages)>3900):
                if accumulated_messages!="":
                    # print(f"sent {len(accumulated_messages)}")
                    asyncio.run_coroutine_threadsafe(self.send_accumulated_messages(accumulated_messages), self.bot.loop)                       
                    accumulated_messages = ""
                    start_time = time.time()
            
        # else:
        #     while True:
        #         try:
        #             output = output_queue.get_nowait()
        #             print(output)
        #         except Empty:
        #             time.sleep(0.1)
       

def setup(bot):
    bot.add_cog(Ready(bot))
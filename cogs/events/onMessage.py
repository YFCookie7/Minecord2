from discord.ext import commands
import mcrcon
import re
from globals import MINECRAFT_CHANNEL_ID, server_host, rcon_password, rcon_port


class onMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
  
    def send_rcon_command(self, command):
        try:
            with mcrcon.MCRcon(server_host, rcon_password, rcon_port) as rcon:
                response = rcon.command(command)
                response = re.sub(r'§.', '', response)
                # print(f"Response from server: {response}")
                return response

        except mcrcon.MCRconException as e:
            print(f"Error: {e}")
            

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        if message.channel.id == MINECRAFT_CHANNEL_ID:
            if message.content.startswith("!"):
                message = message.content[1:]
            else:
                message = f"say {message.author}: {message.content}"
            reply = self.send_rcon_command(message)
            if (len(reply) != 0):
                channel = self.bot.get_channel(MINECRAFT_CHANNEL_ID)
                await channel.send(reply)
            return


def setup(bot):
    bot.add_cog(onMessage(bot))
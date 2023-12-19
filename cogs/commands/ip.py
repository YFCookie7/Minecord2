import discord
from discord.ext import commands
from globals import Sub_Domain, Domain
import requests
import socket
import os

def getHostIP():
    try:
        with requests.Session() as session:
            response = session.get('https://checkip.amazonaws.com/', timeout=5, verify=True)
            response.raise_for_status()
            return response.text.strip()
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve the public IP address:", str(e))
        return None

def get_server_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.error as e:
        return f"Error: {e}"

class IP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Obtain minecraft server IP address")
    async def ip(self, ctx):
        await ctx.defer()
        print(os.getcwd())
        server_domain = f"{Sub_Domain}.{Domain}"
        host_ip = getHostIP()
        server_ip = get_server_ip_address(server_domain)

        reply_message = f"Server Domain: {server_domain}\nHost IP: {host_ip}\nServer IP: {server_ip}"
        await ctx.respond(reply_message)


def setup(bot):
    bot.add_cog(IP(bot))
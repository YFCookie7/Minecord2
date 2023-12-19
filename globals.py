import json

def load_config():
    with open("config.json", "r") as json_file:
        config_data = json.load(json_file)
    return config_data
        

config_data = load_config()

DISCORD_TOKEN = config_data.get("DISCORD_TOKEN", "")
MINECRAFT_CHANNEL_ID = config_data.get("MINECRAFT_CHANNEL_ID", 0)
MINECRAFT_LOG_CHANNEL_ID = config_data.get("MINECRAFT_LOG_CHANNEL_ID", 0)
server_host = config_data.get("server_host", "")
rcon_port = config_data.get("rcon_port", 0)
rcon_password = config_data.get("rcon_password", "")
Sub_Domain = config_data.get("Sub_Domain", "")
Domain = config_data.get("Domain", "")
bot_enabled = False

import discord
from discord import *
import ClientClasses
import random
import ticket
import react_role
import misc_commands

client = ClientClasses.client
token = ClientClasses.token
GUILD_ID = ClientClasses.GUILD_ID
GUILD = None

@client.event
async def on_ready():
	global GUILD
	GUILD = client.get_guild(GUILD_ID.id)
	if GUILD is None:
		print(f"Failed to fetch the guild with ID {GUILD_ID.id}")
	else:
		print(f'We have logged in as {client.user}')
		print(f'Connected to guild: {GUILD.name}')
	print(f'----------------------------------\n')

client.run(token)

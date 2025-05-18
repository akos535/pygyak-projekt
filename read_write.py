import os
from discord import *
import discord

GUILD_ID = None
token = None
admin_id = None
mod_id = None
ticket_category_id = None

def get_id():
	global GUILD_ID, token, admin_id, mod_id, ticket_category_id
	if os.path.exists("id.txt"):
		with open("id.txt", "r") as fread:
			GUILD_ID = discord.Object(int(fread.readline()))
			token = fread.readline()
			admin_id = int(fread.readline())
			mod_id = int(fread.readline())
			ticket_category_id = int(fread.readline())
	else:
		guild = input("Guild ID: \n").strip()
		token = input("Token: \n").strip()
		admin_id = input("Admin Role ID: \n").strip()
		mod_id = input("Mod Role ID: \n").strip()
		ticket_category_id = input("Ticket Category ID: \n").strip()
		with open("id.txt", "w") as fwrite:
			fwrite.write(guild + "\n")
			fwrite.write(token)
			if admin_id is not None:
				fwrite.write("\n"+ str(admin_id))
			if mod_id is not None:
				fwrite.write("\n"+ str(mod_id))
			if ticket_category_id is not None:
				fwrite.write("\n" + str(ticket_category_id))
	return GUILD_ID, token, admin_id, mod_id, ticket_category_id
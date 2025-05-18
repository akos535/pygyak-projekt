import discord
import read_write
from ClientClasses import admin_id
from discord import *
import ClientClasses
import asyncio


client = ClientClasses.client
token = ClientClasses.token
GUILD_ID = ClientClasses.GUILD_ID
category_id = ClientClasses.ticket_category_id
admin_role_id = ClientClasses.admin_id
mod_role_id = ClientClasses.mod_id
GUILD = None
ticket_count = 0

# Makes it so users don't see it
def get_overwrites():
	global GUILD, admin_role_id, mod_role_id
	return {
		GUILD.default_role: discord.PermissionOverwrite(read_messages=False),
		GUILD.get_role(admin_role_id): discord.PermissionOverwrite(read_messages=True),
		GUILD.get_role(mod_role_id): discord.PermissionOverwrite(read_messages=True),
	}

def ticket_name():
	global ticket_count
	ticket_count += 1
	return f'ticket-{str(ticket_count)}'

@client.tree.command(name='report')
async def open_ticket(interaction: discord.Interaction):
	global GUILD, admin_role_id, mod_role_id, category_id
	await client.wait_until_ready()
	GUILD = client.get_guild(GUILD_ID.id)
	overwrite = get_overwrites()

	# Making the ticket accessible for the user who created it
	overwrite.update({interaction.user: discord.PermissionOverwrite(read_messages=True)})
	category = GUILD.get_channel(category_id)
	new_ticket = await GUILD.create_text_channel(f'{ticket_name()}', overwrites=overwrite, category=category)

	# Send a reply if the ticket was created successfully
	if new_ticket is not None:
		await interaction.response.send_message(f'Ticket created, please continue your report in <#{new_ticket.id}>', ephemeral=True)
		await new_ticket.send(f'This ticket was created by {interaction.user.mention}, please wait for an admin or moderator to respond.\n<@&{admin_role_id}> <@&{mod_role_id}>')

	# checking if the user sending the close message is a moderator or admin
	def check(message: discord.Message):
		if message.channel == new_ticket and message.content == "+close":
			for role in message.author.roles:
				if role.id == admin_role_id or role.id == mod_role_id:
					return True

	# waiting for the close message to be sent
	try:
		await client.wait_for('message', check=check, timeout=600000)
		await new_ticket.delete(reason="problem resolved, ticket closed")
	except asyncio.TimeoutError:
		await new_ticket.delete(reason="Ticket timeout")
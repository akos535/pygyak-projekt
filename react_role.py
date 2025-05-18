import discord
from ClientClasses import admin_id
from discord import *
import ClientClasses

client = ClientClasses.client
admin_role_id = ClientClasses.admin_id

role_message = None
EMOJI_ROLE = None
@client.tree.command(name="react_roles")
@app_commands.checks.has_role(admin_role_id)
async def react_roles(interaction: discord.Interaction):
	global role_message, EMOJI_ROLE
	await client.wait_until_ready()
	EMOJI_ROLE = {
		"🟩": 1371860332229951488,
		"🟥": 1371860415658725439,
		"🟦": 1371860488358592592
	}

	embed = discord.Embed(title="React to get roles",
						  description="\n\n".join(f'{emoji} - <@&{role_id}>' for emoji, role_id in EMOJI_ROLE.items()),
						  colour=Colour.from_rgb(50, 255, 50))
	role_message = await interaction.channel.send(embed=embed)
	# goes through EMOJI_ROLE and adds the reactions
	for emoji, role_id in EMOJI_ROLE.items():
		await role_message.add_reaction(emoji)
	# Sends a message to the user that the reaction roles are ready
	await interaction.response.send_message("Reaction role message ready.", ephemeral=True)

# Checks who added the reaction and gives the role
@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
	global role_message
	if (payload.message_id == role_message.id) and (role_message is not None) and (payload.user_id is not client.user.id):
		guild = client.get_guild(payload.guild_id)
		role = guild.get_role(EMOJI_ROLE[payload.emoji.name])
		member = guild.get_member(payload.user_id) or await guild.fetch_member(payload.user_id)
		await member.add_roles(role)

# Checks who removed the reaction and removes the role
@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
	global role_message
	if (payload.message_id == role_message.id) and (role_message is not None) and (payload.user_id is not client.user.id):
		guild = client.get_guild(payload.guild_id)
		role = guild.get_role(EMOJI_ROLE[payload.emoji.name])
		member = guild.get_member(payload.user_id) or await guild.fetch_member(payload.user_id)
		await member.remove_roles(role)
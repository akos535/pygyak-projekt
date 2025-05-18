import discord
from discord import *
import ClientClasses
import random
import asyncio
import pyfiglet
import datetime

client = ClientClasses.client

@client.tree.command(name="guess")
async def number_guesser(interaction : discord.Interaction):
	await client.wait_until_ready()
	await interaction.response.send_message(f'Guess the number 1-10 (Only send an number!)\nYou have 20 seconds to guess.', ephemeral=True)
	number = random.randint(1, 10)
	msg = None
	print(f'The number {interaction.user.name} has to guess: {number}')
	def check(message: discord.Message):
		return message.author.id == interaction.user.id and message.channel.id == interaction.channel_id

	try:
		msg = await client.wait_for('message', check=check, timeout=20.0)
	except asyncio.TimeoutError:
		await interaction.followup.send(f'You ran out of time', ephemeral=True)

	# Checks if the user guessed the number correctly
	# if the user guessed the number incorrectly, they get timed out for 3 minutes
	if msg.content.strip() == str(number):
		await msg.delete()
		await interaction.followup.send(f'You guessed the number correctly!', ephemeral=True)
	else:
		await msg.delete()
		await interaction.user.timeout(discord.utils.utcnow()+datetime.timedelta(minutes=3) ,reason="Guessed wrong")
		await interaction.followup.send(f'You guessed the number wrong, the number was {number}', ephemeral=True)


@client.tree.command(name="remindme")
async def remind_me(interaction: discord.Interaction):
	await client.wait_until_ready()
	await interaction.response.send_message(f'Please send me the time you want to be reminded in minutes\nThe format:\n`reminder text, minutes`')
	msg = None

	def check(message: discord.Message):
		return message.author.id == interaction.user.id and message.channel.id == interaction.channel_id

	try:
		msg = await client.wait_for('message', check=check, timeout=30.0)
	except asyncio.TimeoutError:
		await interaction.followup.send(f'You ran out of time.', ephemeral=True)

	if msg is not None:
		reminder_text = msg.content.split(",")[0]
		reminder_minutes = msg.content.split(",")[1].strip()
		await msg.reply(f'You will be reminded about "{reminder_text}" in {reminder_minutes} minutes')
		await asyncio.sleep(int(reminder_minutes)*60)
		await interaction.followup.send(f'<@{interaction.user.id}> \"{reminder_text}\"')


@client.tree.command(name="ascii")
async def ascii(interaction: discord.Interaction):
	await client.wait_until_ready()
	await interaction.response.send_message(f'Please send me the text you want to convert to ascii art')
	msg = None

	def check(message: discord.Message):
		return message.author.id == interaction.user.id and message.channel.id == interaction.channel_id

	try:
		msg = await client.wait_for('message', check=check, timeout=30.0)
	except asyncio.TimeoutError:
		await interaction.followup.send(f'You ran out of time.', ephemeral=True)

	if msg is not None:
		text = msg.content
		await interaction.channel.send(f'<@{interaction.user.id}>\nHere is your ascii art:\n```{pyfiglet.figlet_format(text, font="slant")}```')
import discord
from discord import app_commands
import read_write


class MyClient(discord.Client):
    def __init__(self, guild_id: discord.Object, intents: discord.Intents):
        super().__init__(intents=intents)
        self.guild_id = guild_id
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=self.guild_id)
        await self.tree.sync(guild=self.guild_id)


GUILD_ID, token, admin_id, mod_id, ticket_category_id = read_write.get_id()
intent = discord.Intents.default()
intent.message_content = True
intent.reactions = True
client = MyClient(GUILD_ID, intents=intent)
import discord
from discord import app_commands
from discord.ext import commands
from utils.anilist.pagination import ButtonView
from utils.anilist.create_embed import create_embeds
from utils.anilist.fetch_anilist_data import create_entries_list, fetch_anilist_data, get_username

class Anilist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("anilist.py is ready!")

    @app_commands.command(name="anilist-profile", description="Displays anilist profile")
    async def anilist(self, interaction: discord.Interaction, username: str):
        data = fetch_anilist_data(username)

        anilist_username = get_username(data)
        entries = create_entries_list(data)

        embeds = create_embeds(entries, anilist_username)

        
        view = ButtonView(embeds)
        await interaction.response.send_message(embed=embeds[0], view=view)
        

async def setup(bot):
    await bot.add_cog(Anilist(bot))
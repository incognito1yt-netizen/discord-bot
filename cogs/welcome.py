import discord
from discord.ext import commands
from discord import app_commands
import json
import os

CONFIG_FILE = "welcome_channels.json"

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Wczytanie konfiguracji z pliku JSON
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                self.welcome_channels = json.load(f)
        else:
            self.welcome_channels = {}

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.welcome_channels, f, indent=4)

    # Slash command
    @app_commands.command(name="autowelcome", description="Ustaw kanał powitalny dla nowych użytkowników")
    @app_commands.describe(channel="Kanał, do którego będą wysyłane powitania")
    async def autowelcome(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = str(interaction.guild.id)
        self.welcome_channels[guild_id] = channel.id
        self.save_config()
        await interaction.response.send_message(f"✅ Kanał powitalny ustawiony na {channel.mention}", ephemeral=True)

    # Listener dla nowych członków
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild_id = str(member.guild.id)
        if guild_id not in self.welcome_channels:
            return

        channel_id = self.welcome_channels[guild_id]
        channel = member.guild.get_channel(channel_id)
        if not channel:
            return

        embed = discord.Embed(
            title="🎉 Witamy na serwerze!",
            description=f"Witaj {member.mention}! Cieszymy się, że do nas dołączyłeś.",
            color=discord.Color.blue()
        )

        # Dodanie ikony serwera
        if member.guild.icon:
            embed.set_thumbnail(url=member.guild.icon.url)
        # Dodanie bannera serwera, jeśli istnieje
        if member.guild.banner:
            embed.set_image(url=member.guild.banner.url)

        await channel.send(embed=embed)

# Setup cog poprawnie z await
async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))

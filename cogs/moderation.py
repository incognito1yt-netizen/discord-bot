import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Usuń określoną liczbę wiadomości")
    @app_commands.describe(amount="Ile wiadomości chcesz usunąć")
    async def clear(self, interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("❌ Nie masz uprawnień.", ephemeral=True)
            return

        deleted = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"✅ Usunięto {len(deleted)} wiadomości.", ephemeral=True)

    @app_commands.command(name="clearall", description="Usuń wszystkie wiadomości w kanale")
    async def clearall(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("❌ Nie masz uprawnień.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=None)
        await interaction.followup.send(f"🧹 Ukończono czyszczenie. Usunięto {len(deleted)} wiadomości.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))

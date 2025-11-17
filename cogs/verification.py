import discord
from discord.ext import commands
from discord import app_commands
import random

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="verifychannel", description="Ustaw kanał weryfikacyjny i rolę")
    @app_commands.describe(channel="Kanał weryfikacyjny", role="Rola, którą użytkownik otrzyma")
    async def verifychannel(self, interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role):

        # Embed z ładną wiadomością
        embed = discord.Embed(
            title="🛡️ Weryfikacja serwera",
            description=f"Aby uzyskać rolę {role.mention}, kliknij przycisk poniżej i rozwiąż quiz matematyczny.",
            color=discord.Color.green()
        )
        embed.set_footer(text="Twoja rola zostanie nadana po poprawnym rozwiązaniu quizu.")

        # Unikalny przycisk
        button = discord.ui.Button(label="Zweryfikuj się", style=discord.ButtonStyle.success, custom_id=f"verify-{role.id}-{random.randint(1,10000)}")

        async def button_callback(interaction2: discord.Interaction):
            # Quiz matematyczny
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            c = random.randint(1, 10)
            wynik = a + b * c

            # Modal
            class MathModal(discord.ui.Modal, title="🧮 Quiz weryfikacyjny"):
                answer = discord.ui.TextInput(label=f"Oblicz wynik: {a} + {b} x {c}", style=discord.TextStyle.short)

                async def on_submit(self, modal_interaction: discord.Interaction):
                    try:
                        if int(self.answer.value) == wynik:
                            await modal_interaction.user.add_roles(role)
                            await modal_interaction.response.send_message(f"✅ Zweryfikowano! Otrzymałeś rolę {role.mention}", ephemeral=True)
                        else:
                            await modal_interaction.response.send_message("❌ Błędny wynik. Spróbuj ponownie.", ephemeral=True)
                    except discord.Forbidden:
                        await modal_interaction.response.send_message("❌ Bot nie ma uprawnień do nadawania roli.", ephemeral=True)

            await interaction2.response.send_modal(MathModal())

        button.callback = button_callback
        view = discord.ui.View()
        view.add_item(button)

        # Wysyłamy embed z przyciskiem do kanału weryfikacyjnego
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"✅ Wiadomość weryfikacyjna wysłana do {channel.mention} z rolą {role.mention}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Verification(bot))

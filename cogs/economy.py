import discord, random
from discord.ext import commands
from discord import app_commands
from utils.database import get_balance, add_coins

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance")
    async def balance(self, i: discord.Interaction):
        bal = await get_balance(i.guild.id, i.user.id)
        await i.response.send_message(f"{bal} coins")

    @app_commands.command(name="work")
    async def work(self, i: discord.Interaction):
        reward = random.randint(20, 50)
        await add_coins(i.guild.id, i.user.id, reward)
        await i.response.send_message(f"Earned {reward}")

async def setup(bot):
    await bot.add_cog(Economy(bot))

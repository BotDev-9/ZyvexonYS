import discord, requests, os
from discord.ext import commands
from discord import app_commands
from utils.database import get_channels, get_balance, add_coins, is_premium
from utils.config import CONFIG

API = os.getenv("OPENROUTER_API_KEY")

def ask(prompt):
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API}"},
        json={
            "model": "meta-llama/llama-3-8b-instruct:free",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return r.json()["choices"][0]["message"]["content"][:200]

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def allowed(self, i):
        ch = await get_channels(i.guild.id)
        if i.channel.id not in ch:
            await i.response.send_message("Not enabled")
            return False
        return True

    @app_commands.command(name="chat")
    async def chat(self, i: discord.Interaction, msg: str):
        if not await self.allowed(i): return
        await i.response.defer()
        reply = ask(msg)
        await i.followup.send(reply)

    @app_commands.command(name="roast")
    async def roast(self, i: discord.Interaction, user: discord.Member):
        if not await self.allowed(i): return

        cost = CONFIG["AI_COST"]["roast"]
        bal = await get_balance(i.guild.id, i.user.id)

        if bal < cost:
            await i.response.send_message("Need coins")
            return

        await add_coins(i.guild.id, i.user.id, -cost)

        await i.response.defer()
        reply = ask(f"Roast {user.name}")
        await i.followup.send(reply)

async def setup(bot):
    await bot.add_cog(AI(bot))

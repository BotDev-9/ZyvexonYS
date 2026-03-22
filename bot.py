import discord, os
from discord.ext import commands
from dotenv import load_dotenv
from utils.database import setup_db

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await setup_db()
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()

async def load():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

def run_bot():
    import asyncio
    async def main():
        async with bot:
            await load()
            await bot.start(os.getenv("DISCORD_TOKEN"))
    asyncio.run(main())

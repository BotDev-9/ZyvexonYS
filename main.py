import threading
import asyncio
import os

from dashboard import app
from bot import bot, load  # make sure bot.py has these

# Run Discord bot
def run_bot():
    async def start_bot():
        async with bot:
            await load()
            await bot.start(os.getenv("DISCORD_TOKEN"))

    asyncio.run(start_bot())

# Run Flask dashboard
def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Start bot in background thread
    threading.Thread(target=run_bot, daemon=True).start()

    # Run web server (main thread)
    run_web()
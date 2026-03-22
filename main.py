import threading
import bot
import dashboard

def run_bot():
    bot.run_bot()

def run_web():
    dashboard.app.run(host="0.0.0.0", port=5000)

threading.Thread(target=run_bot).start()
threading.Thread(target=run_web).start()

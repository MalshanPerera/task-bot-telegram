from bot import create_bot

if __name__ == "__main__":
    try:
        bot = create_bot()
        print("✅ Task bot is running...")
        bot.run_polling()
    except Exception as e:
        print(f"❌ Error starting the bot: {e}")

from bot import create_bot

if __name__ == "__main__":
    try:
        app = create_bot()

        # remove any webhook you may have set previously
        # (if create_bot() returns an Application)
        app.bot.delete_webhook(drop_pending_updates=True)

        print("✅ Task bot is running...")
        app.run_polling()
    except Exception as e:
        print(f"❌ Error starting the bot: {e}")

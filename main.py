import time
import logging
from telegram.error import NetworkError
from bot import create_bot

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s — %(levelname)s — %(message)s", level=logging.INFO
    )

    while True:
        try:
            bot = create_bot()
            logging.info("✅ Task bot is starting…")
            # This will block until you Ctrl‑C or an unrecoverable error occurs
            bot.run_polling()
            # If run_polling ever returns normally, break out of the loop
            break
        except NetworkError as e:
            logging.warning("🌐 NetworkError (Bad Gateway) encountered: %s", e)
            logging.info("⏳ Sleeping 5s before restarting polling…")
            time.sleep(5)
        except Exception:
            logging.exception("💥 Unhandled exception, exiting")
            break

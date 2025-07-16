import telebot
import re

API_TOKEN = '7456361483:AAEbZNRtbh53bvgS6DfJXdE6zb46qiWShZc'  # Reemplaza esto por tu token real

bot = telebot.TeleBot(API_TOKEN)

whitelist_urls = []
url_regex = r"(https?://\S+)"

@bot.message_handler(func=lambda message: True)
def check_message(message):
    try:
        if message.chat.type in ["group", "supergroup"]:
            text_to_check = message.text or message.caption or ""

            if message.forward_from and hasattr(message.forward_from, 'text'):
                text_to_check = message.forward_from.text

            if text_to_check:
                matches = re.findall(url_regex, text_to_check)
                if matches:
                    for url in matches:
                        if url not in whitelist_urls:
                            try:
                                username = ""
                                if message.forward_from:
                                    username = message.forward_from.first_name or f"User (ID:{message.forward_from.id})"
                                else:
                                    username = message.from_user.first_name or f"User (ID:{message.from_user.id})"

                                warning_msg = bot.send_message(
                                    message.chat.id,
                                    f"⚠️ Warning, {username}! Links are not allowed in this group.",
                                    reply_to_message_id=message.message_id
                                )

                                bot.delete_message(message.chat.id, message.message_id)

                            except telebot.apihelper.ApiTelegramException as e:
                                if e.error_code == 403:
                                    bot.send_message(
                                        message.chat.id,
                                        "⚠️ I don't have permission to delete messages. Please make me an admin."
                                    )
                                else:
                                    print(f"API Error: {e}")
                            except Exception as e:
                                print(f"Unexpected error: {e}")
    except Exception as e:
        print(f"General error: {e}")

if __name__ == '__main__':
    print("Starting bot...")
    bot.infinity_polling()
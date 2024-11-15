import easy_tg_bot
import requests

# initiate other modules
import settings

# debug
import logging
logging.basicConfig(level=logging.INFO)    

@easy_tg_bot.command()
async def help(update, context):
    return await easy_tg_bot.send_message(update, context, text_string_index = "help_message", replace=False)  # text.xlsx

@easy_tg_bot.message_handler()
async def handle_message(update, context):
    text = update.message.text
    payload = {"text": text}
    response = requests.post("http://mainapi:8000/echo", json=payload)
    if response.status_code == 200:
        response_json = response.json()
        new_text = response_json.get("text", "")
        return await easy_tg_bot.send_message(update, context, text=new_text, replace=False)
    else:
        logging.error(f"Request failed with status code {response.status_code}")
        return await easy_tg_bot.send_message(update, context, text="Error: Unable to process your request.")

if __name__=="__main__":
    easy_tg_bot.start.START_DONE_CALLBACK = help
    easy_tg_bot.telegram_bot_polling()

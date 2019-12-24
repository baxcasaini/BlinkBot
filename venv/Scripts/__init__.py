import traceback
import requests
import re
import json
import cv2

from pyzbar import pyzbar
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def get_image_url():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


def bop(bot, update):
    url = get_image_url()
    chat_id = update.message.chat_id
    bot.send_text(chat_id=chat_id, photo=url)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def receivePhoto(update, context):
    try:
        big_img = update.message.photo[-1]
        new_file = big_img.bot.get_file(big_img.file_id)
        path = new_file.file_path.split("/")
        new_file.download(path[6])

        img = cv2.imread(path[6])
        decoded = pyzbar.decode(img)
    except Exception as err:
        traceback.print_tb(err.__traceback__)
        pass

    update.message.text = decoded[0].data.decode("utf-8")
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def main():
    updater = Updater('982491961:AAHnxYKVvKaW2SDFIQH8h21hTyMHAj3wpC0', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.photo, receivePhoto))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()


'In attesa di nuovi messaggi...'

if __name__ == '__main__':
    main()
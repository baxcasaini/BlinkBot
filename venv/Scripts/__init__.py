import traceback
import requests
import re
import json
import cv2

from pyzbar import pyzbar
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import time

import telepot

TOKEN = '982491961:AAHnxYKVvKaW2SDFIQH8h21hTyMHAj3wpC0'

# creazione dell’oggetto di tipo bot

bot = telepot.Bot(TOKEN)
authenticated = False


# dichiarazione funzione handle
def handle(msg):
    global authenticated
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        if msg['text'] == '/start':
            contact_keyboard = KeyboardButton(text="Share contact",
                                              request_contact=True)  # creating contact button object
            custom_keyboard = [[contact_keyboard]]  # creating keyboard object

            bot.sendMessage(chat_id, 'Please autheticate yourself',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=custom_keyboard
                            ))
        elif not authenticated:
            bot.sendMessage(chat_id, "Authenticate yourself to continue")

    if content_type == 'contact':

        response = requests.get("http://localhost:8080/login/check/" + msg['contact']['phone_number'])

        if response.status_code == 200 and response.content is not None:
            bot.sendMessage(chat_id, 'Authenticated !', reply_markup=ReplyKeyboardRemove())
            location_keyboard = KeyboardButton(text="Please provide your actual location every time",
                                               request_location=True)  # creating location button object
            custom_keyboard = [[location_keyboard]]  # creating keyboard object

            bot.sendMessage(chat_id, 'Now you can share your location',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=custom_keyboard
                            ))
            authenticated = True;
        else:
            bot.sendMessage(chat_id, "Something went wrong with your authentication")

    if authenticated:
        if content_type == 'photo':
            try:
                new_file = bot.download_file(msg['photo'][-1]['file_id'], 'image.png')
                img = cv2.imread('image.png')
                decoded = pyzbar.decode(img)
                text = decoded[0].data.decode("utf-8")
                bot.sendMessage(chat_id, text)

            except Exception as err:
                traceback.print_tb(err.__traceback__)
                pass


def handleAll():
    # per ogni messaggio ricevuto viene aperta un’istanza della funzione handle

    bot.message_loop(handle)

    print('Listening ...')

    # diamo 10 secondi di pausa

    while 1:
        time.sleep(1)


def main():
    handleAll()


'In attesa di nuovi messaggi...'

if __name__ == '__main__':
    main()

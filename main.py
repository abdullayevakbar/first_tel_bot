import requests
from pprint import pprint
from Token import token
TOKEN = token


class Messages:
    def __init__(self, TOKEN):
        self.TOKEN = TOKEN

    def get_updates(self):
        r = requests.get(
            f'https://api.telegram.org/bot{self.TOKEN}/getUpdates')
        updates = r.json()
        return updates

    def send_message(self, chat_id):
        url = f'https://api.telegram.org/bot{self.TOKEN}/sendMessage'
        line1 = [{'text': '👥 Users'}, {'text': '🏷 Orders'}]
        line2 = [{'text': '👋 Welcome text'}, {'text': '🖼 Set logo'}]
        line3 = [{'text': '➕ Add Category'},
                 {'text': '🗑 Remove Category'}]
        line4 = [{'text': '📦 New product'}, {'text': '🗑 Delete product'}]
        keyboard = [line1, line2, line3, line4]
        data = {
            'chat_id': chat_id,
            'text': "You can look at the keyboard!",
            'reply_markup': {"keyboard": keyboard, 'resize_keyboard': True}
        }
        requests.post(url, json=data)

    def send_photo(self, text, chat_id):
        url = f'https://api.telegram.org/bot{self.TOKEN}/sendPhoto'
        if text == 'cat':
            r = requests.get('https://aws.random.cat/meow')
            data = r.json()
            img_url = data.get('file')
            data = {
                'chat_id': chat_id,
                'photo': img_url,
                'caption': f"<i><b>#CAT</b></i>",
                'parse_mode': 'HTML'
            }
            requests.post(url, data=data)
        else:
            r = requests.get('https://dog.ceo/api/breeds/image/random')
            data = r.json()
            img_url = data.get('message')
            data = {
                'chat_id': chat_id,
                'photo': img_url,
                'caption': f"<i><b>#DOG</b></i>",
                'parse_mode': 'HTML'
            }
            requests.post(url, data=data)

    def send_contact(self, chat_id, text):
        url = f'https://api.telegram.org/bot{TOKEN}/sendContact'
        if text == "contact_1":
            data = {
                'chat_id': chat_id,
                'phone_number': '+998997444358',
                'first_name': "Diyorbek",
                'last_name': 'Fafandiro'
            }
        elif text == "contact_2":
            data = {
                'chat_id': chat_id,
                'phone_number': '+998943577744',
                'first_name': "Javohir",
                'last_name': 'Jalilov'
            }
        else:
            data = {
                'chat_id': chat_id,
                'phone_number': '+998973935107',
                'first_name': "Akbar",
                'last_name': 'Abdullayev'
            }

        r = requests.post(url, data=data)


def read_txt(last_message, chat_id):
    # if 'contact' in last_message:
    #     f.send_contact(chat_id=chat_id, text=last_message)
    # elif last_message.lower() in ('cat', "dog"):
    #     f.send_photo(text=last_message.lower(), chat_id=chat_id)
    # else:
    f.send_message(chat_id=chat_id)


f = Messages(TOKEN)
old_last_message_id = -1
while True:
    data = f.get_updates()

    message_data = data['result'][-1]['message']

    last_message_id = message_data['message_id']

    chat_id = message_data['chat']['id']

    if last_message_id != old_last_message_id:

        old_last_message_id = last_message_id
        read_txt(message_data['text'], chat_id)

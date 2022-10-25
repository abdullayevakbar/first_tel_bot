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

    def send_message(self, text, chat_id):
        url = f'https://api.telegram.org/bot{self.TOKEN}/sendMessage'
        # line1 = [{'text': '🏬 Catalog'}, {'text': '📦 Orders'}]
        # line2 = [{'text': '👤 Userinfo'}, {'text': '🛒 Card'}]
        # line3 = [{'text': '🎛 Administration demo'}]
        # line4 = [{'text': '📦 New product'}, {'text': '🗑 Delete product'}]
        # keyboard = [line1, line2, line3]
        data = {
            'chat_id': chat_id,
            'text': text
            # 'reply_markup': {"keyboard": keyboard, 'resize_keyboard': True}
        }
        requests.post(url, json=data)

    def reply(self, data1, chat_id):
        list_keys = list(data1.keys())
        url = f'https://api.telegram.org/bot{self.TOKEN}/send{list_keys[-1].title()}'
        print(url)
        pprint(data1[list_keys[-1]])
        if list_keys[-1] == 'contact':
            data = data1[list_keys[-1]]
            del data['user_id']
            data['chat_id'] = chat_id
        elif type(data1[list_keys[-1]]) == type([]):

            data2 = data1[list_keys[-1]][0]
            data = {
                'chat_id': chat_id,
                f'{list_keys[-1]}': data2['file_id']
            }
        else:
            data2 = data1[list_keys[-1]]
            data = {
                'chat_id': chat_id,
                f'{list_keys[-1]}': data2['file_id']
            }

        pprint(data)
        requests.post(url, json=data)
        pass

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


def read_txt(last_message_data, chat_id):
    # if 'contact' in last_message:
    #     f.send_contact(chat_id=chat_id, text=last_message)
    # elif last_message.lower() in ('cat', "dog"):
    #     f.send_photo(text=last_message.lower(), chat_id=chat_id)
    # else:
    list_keys = list(last_message_data.keys())
    print(list_keys)
    if list_keys[-1] == 'text':
        f.send_message(text=last_message_data['text'], chat_id=chat_id)
    else:
        f.reply(last_message_data, chat_id)
    # f.send_message(chat_id=chat_id, data=last_message_data)


f = Messages(TOKEN)
old_last_message_id = -1
while True:
    data = f.get_updates()

    message_data = data['result'][-1]['message']

    last_message_id = message_data['message_id']

    chat_id = message_data['chat']['id']

    if last_message_id != old_last_message_id:

        old_last_message_id = last_message_id
        read_txt(message_data, chat_id)

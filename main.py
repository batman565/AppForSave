import requests
from pprint import pprint
import json
from tqdm import tqdm
import time


token = ''


class VK:
    def __init__(self, access_token, user_id, version='5.199'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': 'profile', 'extended': '1'}
        response = requests.get(url, params={**self.params, **params})
        return response.json()


class Yandex:
    def __init__(self, acc_token):
        self.token = acc_token

    def create_folder(self, path):
        url_create = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {
            'path': path
        }
        headers = {
            'Authorization': self.token
        }
        return requests.put(url_create, params=params, headers=headers)

    def upload_photos(self, filename, path):
        url_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'path': f'{path}/{filename}',
            'overwrite': 'true'
        }
        headers = {
            'Authorization': self.token
        }
        response = requests.get(url_upload, params=params, headers=headers)
        upload_link = response.json()['href']
        with open(pathfile, 'rb') as f:
            return requests.put(upload_link, files={'file': f})


acc_token = input("Введите ваш Токен Яндекс диска: ")
user_id = input("Введите ваш id в ВК: ")
path = input("Введите путь в формате (/path/...): ")
access_token = token
vk = VK(access_token, user_id)
count = int(vk.get_photos()['response']['count'])
data = {'photo': []}
count_user = int(input("Введите количество фотографий для сохранения: "))

if count_user <= count:
    for i in range(0, count_user):
        photo = (vk.get_photos()['response']['items'][i]['orig_photo']['url'])
        likes = (vk.get_photos()['response']['items'][i]['likes']['count'])
        size_h = (vk.get_photos()['response']['items'][i]['orig_photo']['height'])
        size_w = (vk.get_photos()['response']['items'][i]['orig_photo']['width'])
        filename = f'{likes}.jpg'
        pathfile = f'savedVK/{filename}'

        img_data = requests.get(photo).content
        with open(pathfile, 'wb') as handler:
            handler.write(img_data)

        yandex = Yandex(acc_token)
        yandex.create_folder(path)
        yandex.upload_photos(filename, path)

        data['photo'].append({'filename': filename,
                              'size': f'Height: {size_h}, width: {size_w}'})

        with open('photo.json', 'w') as file1:
            json.dump(data, file1)

        for n in tqdm(range(100)):
            time.sleep(0.01)

    with open('photo.json') as json_file:
        data = json.load(json_file)
        pprint(data)
else:
    print("Неверное количество фотографий!")
import requests
from pprint import pprint
import json
from tqdm import tqdm
import time


token_vk = 'Ваш токен ВК'


class VK:
    def __init__(self, access_token, version='5.199'):
        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_photos(self, ids):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': ids, 'album_id': 'profile', 'extended': '1'}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def parse_vk_photos(self, user_id, count_user):
        photos_data = []
        count = int(vk.get_photos(user_id)['response']['count'])

        if count_user <= count:
            for i in range(count_user):
                photo_info = vk.get_photos(user_id)['response']['items'][i]
                photo_url = photo_info['orig_photo']['url']
                likes = photo_info['likes']['count']
                size_h = photo_info['orig_photo']['height']
                size_w = photo_info['orig_photo']['width']
                filename = f'{likes}.jpg'
                pathfile = f'savedVK/{filename}'
                photos_data.append({
                    'url': photo_url,
                    'likes': likes,
                    'size_h': size_h,
                    'size_w': size_w,
                    'filename': filename,
                    'pathfile': pathfile
                })

        return photos_data


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

    def upload_photos(self, fname, path):
        url_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'path': f'{path}/{fname}',
            'overwrite': 'true'
        }
        headers = {
            'Authorization': self.token
        }
        response = requests.get(url_upload, params=params, headers=headers)
        upload_link = response.json()['href']
        with open(photo["pathfile"], 'rb') as f:
            return requests.put(upload_link, files={'file': f})


acc_token = input("Введите ваш Токен Яндекс диска: ")
user_id = str(input("Введите ваш id в ВК: "))
path = input("Введите путь в формате (/path/...): ")
vk = VK(token_vk)
data = {'photo': []}
count_user = int(input("Введите количество фотографий для сохранения: "))

photos_data = vk.parse_vk_photos(user_id, count_user)

if len(photos_data) > 0:
    for photo in photos_data:
        img_data = requests.get(photo['url']).content
        with open(photo["pathfile"], 'wb') as handler:
            handler.write(img_data)

        yandex = Yandex(acc_token)
        yandex.create_folder(path)
        yandex.upload_photos(photo["filename"], path)

        data['photo'].append({'filename': photo['filename'],
                              'size': f'Height: {photo["size_h"]}, width: {photo["size_w"]}'})

        with open('photo.json', 'w') as file1:
            json.dump(data, file1)

        for n in tqdm(range(100)):
            time.sleep(0.01)

    with open('photo.json') as json_file:
        data = json.load(json_file)
        pprint(data)
else:
    print("Неверное количество фотографий!")

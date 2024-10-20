import requests
from pprint import pprint


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


access_token = token
user_id = '390982632'
vk = VK(access_token, user_id)
pprint(vk.get_photos())
# photo = (vk.get_photos()['response']['items'][0]['orig_photo']['url'])

# img_data = requests.get(photo).content
# with open('.jpg', 'wb') as handler:
#     handler.write(img_data)


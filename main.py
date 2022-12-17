import sys

import requests
from settings import TOKEN
import os

FILE_NAME = 'test.txt'
FILE_DIR = 'export'
ROOT_PATH = os.getcwd()


class Yandex:
    host = 'https://cloud-api.yandex.net:443'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_link_for_upload(self, file_name):
        url = self.host + '/v1/disk/resources/upload'
        response = requests.get(
            url, headers=self.get_headers(),
            params={'path': f'/{file_name}'}
        )
        if response:
            return response.json()
        else:
            print('Что то не так c ссылкой для загрузки файла!')
            sys.exit()

    def publish_resource(self, path_file, file_name):
        response = requests.put(
            self.get_link_for_upload(file_name)['href'],
            headers=self.get_headers(),
            data=open(path_file, 'rb')
        )
        print(f'Файл успешно загружен' if response else 'Что то пошло не так!')


if __name__ == '__main__':
    full_path_to_file = os.path.join(ROOT_PATH, FILE_DIR, FILE_NAME)
    uploader = Yandex(TOKEN)
    uploader.publish_resource(full_path_to_file, 'test.txt')

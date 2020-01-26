import random
import requests
from vk_utils import get_posted_comics_names

def save_image(image_url, savename):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(savename, 'wb') as file:
        file.write(response.content)


def get_last_xkcd_comics_number():
    last_comics_url = 'http://xkcd.com/info.0.json'
    response = requests.get(last_comics_url)
    response.raise_for_status()
    last_comics = response.json()
    last_comics_number = last_comics['num']
    return last_comics_number


def get_comics_name(comics_number):
    url = 'https://xkcd.com/{}/info.0.json'.format(comics_number)
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    comics_name = response['title']
    return comics_name


def fetch_comics(comics_number):
    url = 'https://xkcd.com/{}/info.0.json'.format(comics_number)
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    comics_image = response['img']
    comics_name = response['title']
    comics_name += '.png'
    save_image(comics_image, comics_name)
    return comics_name


def fetch_random_comics_for_group(group_name, vk_access_token):
    last_comics_number = get_last_xkcd_comics_number()
    random_comics_number = random.randint(1, last_comics_number)
    posted_comics_names = get_posted_comics_names(group_name, vk_access_token)
    random_comics_name = get_comics_name(random_comics_number)
    while random_comics_name in posted_comics_names:
        random_comics_number = random.randint(1, last_comics_number)
        random_comics_name = get_comics_name(random_comics_number)
    return fetch_comics(random_comics_number)

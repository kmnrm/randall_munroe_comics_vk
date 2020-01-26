import random
import requests
from vk_utils import get_posted_comics_names, check_response

def save_image(image_url, savename):
    response = requests.get(image_url)
    response_text = response.text
    check_response(response_text)
    with open(savename, 'wb') as file:
        file.write(response.content)


def get_last_xkcd_comics_number():
    last_comics_url = 'http://xkcd.com/info.0.json'
    response = requests.get(last_comics_url)
    response_text = response.text
    check_response(response_text)
    last_comics = response.json()
    last_comics_number = last_comics['num']
    return last_comics_number


def get_comics_name(comics_number):
    url = 'https://xkcd.com/{}/info.0.json'.format(comics_number)
    response = requests.get(url)
    response_text = response.text
    check_response(response_text)
    response = response.json()
    comics_name = response['title']
    return comics_name


def fetch_random_comics_for_group(group_name, vk_access_token):
    last_comics_number = get_last_xkcd_comics_number()
    random_comics_number = get_random_comics_number(last_comics_number)
    save_comics_number_to_file(random_comics_number)
    url = 'https://xkcd.com/{}/info.0.json'.format(random_comics_number)
    response = requests.get(url)
    response_text = response.text
    check_response(response_text)
    response = response.json()
    comics_image = response['img']
    comics_name = response['title']
    comics_name += '.png'
    save_image(comics_image, comics_name)    
    return comics_name


def get_random_comics_number(last_comics_number):
    random_comics_number = random.randint(1, last_comics_number)
    posted_comics_nums = get_posted_comics_nums()
    while str(random_comics_number) in posted_comics_nums:
        random_comics_number = random.randint(1, last_comics_number)
    return random_comics_number


def get_posted_comics_nums():
    posted_comics_nums = []
    posted_comics_list_limit = 2000
    wipe_off_quantity = 500
    try:
        with open('posted_comics.txt', 'r') as posted_comics:
            posted_comics_nums = posted_comics.read().split('\n')
            if len(posted_comics_nums) >= posted_comics_list_limit:
                remaining_nums = posted_comics_nums[wipe_off_quantity:]
                posted_comics_nums = refresh_list_of_posted_comics(remaining_nums)
    except FileNotFoundError:
        pass   
    return posted_comics_nums


def save_comics_number_to_file(comics_number):
    with open('published_comics.txt', 'a') as file:
        file.write(str(comics_number) + '\n')


def refresh_list_of_posted_comics(new_nums):
    with open('posted_comics.txt', 'w') as posted_comics:
        for new_num in new_nums:
            posted_comics.write("%s\n" % new_num)
    with open('posted_comics.txt', 'r') as posted_comics:
        refreshed_posted_comics_nums = posted_comics.read().split('\n')
    return refreshed_posted_comics_nums

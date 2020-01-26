import os
from dotenv import load_dotenv
from xkcd_utils import fetch_random_comics_for_group
from vk_utils import post_comics_on_groupwall, remove_comics_image_from_catalog

def main():
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    group_name = 'Комиксы Рэндела Манро'
    try:
        comics_name = fetch_random_comics_for_group(group_name, vk_access_token)
        post_comics_on_groupwall(comics_name, group_name, vk_access_token)
        remove_comics_image_from_catalog(comics_name)
    finally:
        for file in os.listdir():
            if file.endswith('.png'):
                os.remove(file)

if __name__ == '__main__':
    load_dotenv()
    main()

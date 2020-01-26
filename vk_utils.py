import os
import requests

VK_API = 'https://api.vk.com/method/'
VERSION = '5.103'

def get_group_id(group_name, vk_access_token):
    method = 'groups.get'
    groups_url = '{}{}'.format(VK_API, method)
    payload = {
        'extended': 1,
        'filter': 'admin',
        'v': VERSION,
        'access_token': vk_access_token
    }
    response = requests.get(groups_url, params=payload)
    response.raise_for_status()
    response = response.json()
    groups = response['response']['items']
    for group in groups:
        name = group['name']
        if name == group_name:
            group_id = group['id']
    return group_id


def get_posted_comics_names(group_name, vk_access_token):
    method = 'wall.get'
    request_url = '{}{}'.format(VK_API, method)
    group_id = get_group_id(group_name, vk_access_token)
    payload = {
        'owner_id': -group_id,
        'filter': 'owner',
        'v': VERSION,
        'access_token': vk_access_token
    }
    response = requests.get(request_url, params=payload)
    response = response.json()
    posts = response['response']['items']
    comics_names = [post['text'] for post in posts]
    return comics_names


def get_image_upload_url(group_name, vk_access_token):
    method = 'photos.getWallUploadServer'
    request_url = '{}{}'.format(VK_API, method)
    group_id = get_group_id(group_name, vk_access_token)
    payload = {
        'group_id': group_id,
        'v': VERSION,
        'access_token': vk_access_token
        }
    response = requests.get(request_url, params=payload)
    response.raise_for_status()
    response = response.json()
    upload_url = response['response']['upload_url']
    return upload_url


def upload_comics(comics_name, group_name, vk_access_token):
    upload_url = get_image_upload_url(group_name, vk_access_token)
    with open(comics_name, 'rb') as comics:
        files = {'photo': comics}
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    uploaded_comics = response.json()
    os.remove(comics_name)
    return uploaded_comics


def save_comics_for_group(comics_name, group_name, vk_access_token):
    method = 'photos.saveWallPhoto'
    post_url = '{}{}'.format(VK_API, method)
    group_id = get_group_id(group_name, vk_access_token)
    comics = upload_comics(comics_name, group_name, vk_access_token)
    params = {
        'group_id': group_id,
        'photo': comics['photo'],
        'hash': comics['hash'],
        'server': comics['server'],
        'v': VERSION,
        'access_token': vk_access_token
    }
    response = requests.post(post_url, params=params)
    response.raise_for_status()
    saved_comics = response.json()
    return saved_comics


def post_comics_on_groupwall(comics_name, group_name, vk_access_token):
    method = 'wall.post'
    request_url = '{}{}'.format(VK_API, method)
    group_id = get_group_id(group_name, vk_access_token)
    comics = save_comics_for_group(comics_name, group_name, vk_access_token)['response'][0]
    attachments = 'photo{}_{}'.format(comics['owner_id'], comics['id'])
    comics_name = comics_name.split('.')[0]
    params = {
        'owner_id': -group_id,
        'from_group': 1,
        'message': comics_name,
        'attachments': attachments,
        'v': VERSION,
        'access_token': vk_access_token
    }
    response = requests.post(request_url, params=params)
    response.raise_for_status()
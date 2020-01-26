# Randall Munroe Comics publisher
 This program automatically posts a random comics image from [Randall Munroe Comics](https://xkcd.com) on user's pre-created community wall on [VK](https://vk.com/about).
 
## Getting started

### Getting access token

In order to be able to use this program several steps should be done by a user via browser:

1. [Create a VK community](https://vk.com/groups?w=groups_create) with any name you want. Try to avoid the names that are equal to the communities' names that you've already been managing, as it may cause issues the program will be running into.

2. [Create a VK app](https://vk.com/editapp?act=create) and choose **`standalone`** platfrom as it is needed to get an **access token**.

3. After you click on `Connect app` button (it appears only if you choose `standalone` platfrom) get your app `client_id` which you can find in your app `settings` **(App ID)** or copy it from url:
```
https://vk.com/editapp?id=your_client_id
```  

4. Get an access token. In a new tab of your browser go to:
```
https://oauth.vk.com/authorize?client_id=YOUR_CLIENT_ID&scope=wall,groups,photos,offline&response_type=token&v=VERSION
```
where `YOUR_CLIENT_ID` is your **App ID** and `VERSION` is a [current version of VK API](https://vk.com/dev/versions).

After successful authorization your browser will be redirected to [https://oauth.vk.com/blank.html](https://oauth.vk.com/blank.html). Access_token and other parameters will be sent in URL part of the link _(COPY_EVERYTHING_YOU_SEE_HERE)_:
```
https://oauth.vk.com/blank.html#access_token=COPY_EVERYTHING_YOU_SEE_HERE&expires_in=0&user_id=USER_ID
```
Your access token mey look like `1h1h1h1h1h1h14h4h4h4h4k4k4k4l6h298f9df9gr9rfj34j9gjerigj399934jtmf9349jgksjr9g29gsog9`.

For more information go to [Implicit Flow for User Access Token](https://vk.com/dev/implicit_flow_user).


### Last preparations
Before launching this program you need to create an `.env` file in `main.py` directory and add your access token:
```
VK_ACCESS_TOKEN=your_access_token
```

Edit `main.py` by adding your community name:
```
def main():
    ...
    group_name = 'Your_community_name'
    ...
```

Preinstall Python3 to use this program.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

## How to use
Run `main.py` script to upload a random comics image and post it on your community wall. Check it out by opening your community page.
You can find your community on [Communities](https://vk.com/groups) page.

Comics images are fetched by their comics numbers.

All the posted comics' numbers are to be stored in `posted_comics.txt` file. If there is an error that stops execution, the number of the comic that was failed to be uploaded is going to be saved anyway. 

Each post has a title which is the same as comic title.

This program works with [xkcd json](https://xkcd.com/json.html) and [vk.com API](https://vk.com/dev).

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).

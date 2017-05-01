import requests
import json
from bs4 import BeautifulSoup
from pytube import YouTube


def write_json(data, filename='vk.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


# download video vk.com
def download_file(url, title):
    r = requests.get(url, stream=True)
    filename = title + '.' + url.split('/')[-1].split('.')[-1]
    with open(filename, 'wb') as file:
        for chunk in r.iter_content(1024000):
            file.write(chunk)


# parsing url video on vk.com
def get_file_vk(url, title):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    video_url = soup.find('div', id='page_wrap').find('source').get('src').split('?')[0]
    download_file(video_url, title)


# download video youtube.com
def get_file_youtube(url):
    yt = YouTube('http://www.youtube.com/watch?v=' + url)
    # Set the desired quality and extension.
    video = yt.get('mp4', '720p')
    # Specify the destination folder, the default is the current one
    video.download('./')


def main():
    # The required token of your application vk.Developers https://vk.com/dev/first_guide
    # Example
    # https://oauth.vk.com/authorize?client_id=6008211&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=video,photos&response_type=token&v=5.52
    access_token = 'd88d5f1ce6fbf39938baa21659d41ff83f235853afa48f1dac0aeb561d778237e500f2ad591f59d5f22cb'
    # id group or user. If you have screen_name, then you need get id, more https://vk.com/dev/groups.getById
    owner_id = 43948962

    r = requests.get('https://api.vk.com/method/video.get', params={'owner_id': -owner_id,
                                                                    'access_token': access_token, 'album_id': -2})
    # writing to a JSON file
    write_json(r.json())

    videos = r.json()['response'][1:]
    for video in videos:
        if 'vk.com' in video['player']:
            url = video['player']
            title = video['title']
            get_file_vk(url, title)
        if 'youtube.com' in video['player']:
            url = video['player'].split('/')[-1]
            get_file_youtube(url)


if __name__ == '__main__':
    main()

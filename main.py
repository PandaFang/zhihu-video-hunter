# -*- coding:utf-8 -*-

# 知乎视频下载
# 目标网址 https://www.zhihu.com
# @author panda fang
# @date 2018-9-13


import requests
from lxml import etree
import re
import json
import subprocess


QUALITY = 'hd'
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}


def parse_video_ids(url):
    response = requests.get(url, headers = HEADERS).text
    ids = re.findall('data-lens-id="(\d+)"', response)
    # print(response)
    return ids
  

def yield_video_id_and_m3u8_url(video_ids):
    global QUALITY
    for id in video_ids:
        video_url = f'https://lens.zhihu.com/api/videos/{id}'
        response = requests.get(video_url, headers = HEADERS)
        play_list = response.json()['playlist']
        m3u8_url = play_list[QUALITY]['play_url']
        yield id, m3u8_url


def download(save_filename, m3u8_url):
    subprocess.call(['ffmpeg', '-i', m3u8_url, '-c', 'copy', str(save_filename) + '.mp4'])
    pass


def main():
    while True:
        url = input('输入回答链接 如：https://www.zhihu.com/question/267782048/answer/331193600\n>')
        if 'answer' not in url:
            print('可能不是回答的连接')
        else:
            break;

    global QUALITY

    ROW_LEN = 11
    print('-' * ROW_LEN)
    print('| 1. 高清 |')
    print('-' * ROW_LEN)
    print('| 2. 标清 |')
    print('-' * ROW_LEN)
    print('| 3. 低清 |')
    print('-' * ROW_LEN)

    quality = 0
    while quality < 1 or quality > 3:
        try:
            quality = eval(input('请选择要下载的视频质量>'))
        except Exception:
            pass
    if quality == 2:
        QUALITY = 'sd'
    elif quality == 3:
        QUALITY = 'ld'
    else:
        QUALITY = 'hd'

    ids = parse_video_ids(url)
    for m3u8 in yield_video_id_and_m3u8_url(ids):
        download(m3u8[0], m3u8[1])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

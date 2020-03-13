import concurrent.futures
import hashlib
import os
import pathlib
import random
import sys
import time
import urllib.request
from collections import namedtuple
from typing import List

import requests
from tqdm.auto import tqdm

Track = namedtuple('Track', 'idx name url')


class XimaParser:
    def __init__(self, album_index):
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
                  'xm-sign': xm_md5()}
        sort_order = '-1'
        album_size = '1000'
        base_url = 'http://www.ximalaya.com/revision/play/'
        url = base_url + 'album?albumId={}&pageNum=1&sort={}&pageSize={}'.format(album_index, sort_order, album_size)

        req = requests.get(url, headers=header)
        self._tracks_full_info = req.json()['data']['tracksAudioPlay']
        self.album_name = self._tracks_full_info[0]['albumName']

        print(f"{url}\n")
        print(f"Album:\t\t{self.album_name}")

    def get_index_trackname_url(self):
        return [Track(t['index'], t['trackName'], t['src']) for t in self._tracks_full_info]  # debug [:2]


class TqdmUpTo(tqdm):
    """
    Provides `update_to(n)` which uses `tqdm.update(delta_n)`.
    https://github.com/tqdm/tqdm/blob/master/examples/tqdm_wget.py
    """

    def update_to(self, blocks_done=1, each_block_size=1, total_size=None):
        """
        blocks_done  : int, optional
            Number of blocks transferred so far [default: 1].
        each_block_size  : int, optional
            Size of each block (in tqdm units) [default: 1].
        total_size  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if total_size is not None:
            self.total = total_size
        self.update(blocks_done * each_block_size - self.n)  # will also set self.n = b * bsize


def xm_md5():
    url = 'https://www.ximalaya.com/revision/time'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
              'Host': 'www.ximalaya.com'}
    html = requests.get(url, headers=header)
    nowTime = str(round(time.time() * 1000))  # len(nowTime)=13

    sign = f'{hashlib.md5("himalaya-{}".format(html.text).encode()).hexdigest()}' \
           f'({str(round(random.random() * 100))})' \
           f'{html.text}' \
           f'({str(round(random.random() * 100))})' \
           f'{nowTime}'
    return sign


def make_valide_pathname(my_str):
    reserved = '<>:"/|?*\\'
    tt = str.maketrans(reserved, '#' * len(reserved))
    return str(my_str).translate(tt)


def download_and_record_p(my_track: Track):
    global dir_to_save, record_file
    (idx, trackname_raw, url) = my_track

    trackname = trackname_raw.replace(' ', '-')
    file_to_save = os.path.join(dir_to_save,
                                pathlib.Path(f'{idx:03}_{trackname}{os.path.splitext(url)[-1]}'))

    with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, ascii=True,
                  desc=trackname) as t:  # all optional kwargs
        urllib.request.urlretrieve(url, filename=file_to_save, reporthook=t.update_to,
                                   data=None)

    # with tqdm.wrapattr(open(file_to_save, "wb"), "write", miniters=1, desc=trackname) as fout:
    #     r = requests.get(url, stream=True)
    #     r.raise_for_status()  # Replace this with better error handling.
    #     for chunk in r.iter_content(1024):
    #         fout.write(chunk)

    with open(record_file, "a") as ff:
        ff.write(f"{trackname_raw}\n")  # ff.write(f"{idx}\t{trackname}\t{url}\n")


def prepare_download_info(album_idx):
    p = XimaParser(album_idx)

    all_tracks = p.get_index_trackname_url()  # [(idx, name, url), ... ]

    my_dir_to_save = make_valide_pathname(p.album_name)
    my_record_file = os.path.join(my_dir_to_save, '_tmp_record.txt')

    # open record file, create dir/file if not exist
    os.makedirs(my_dir_to_save, exist_ok=True)
    pathlib.Path(my_record_file).touch(exist_ok=True)
    with open(my_record_file, "r") as f:
        done_tracks = f.read().split('\n')

    tracks_do_download: List[Track] = [t for t in all_tracks if t[1] not in done_tracks]  # [ (idx, name, url), ... ]
    # debug
    # tracks_do_download = list(tracks_do_download)[:2]

    return my_dir_to_save, my_record_file, tracks_do_download


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Need an album number, for example:\npython ximalaya3.py 20100404')
        sys.exit()

    print('Fetching album info...')
    dir_to_save, record_file, tracks = \
        prepare_download_info(sys.argv[1].strip())  # album_idx

    if tracks:  # [(idx, trackname, url), ... ]
        print(f'Downloading:\t{len(tracks)} tracks\n')

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(download_and_record_p, tracks)

        print('\nDone')

    else:
        print('All tracks are already downloaded')

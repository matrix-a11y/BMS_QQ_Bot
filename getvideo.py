import os
import sys

import you_get


# url = "https://www.bilibili.com/video/BV1wd4y1V7XV/?spm_id_from=333.788&vd_source=1f25d15ec9536fc381afe59975b1db52/"
# path = "Cachedclips"
def download(url, path):
    sys.argv = ['you-get', '-o', path, url]
    you_get.main()
    for i in os.listdir(path):
        if (i.split('.')[-1] != 'mp4' and i.split('.')[-1] != 'flv'):
            os.remove(path + '/' + i)
    return path + '/' + os.listdir(path)[0]


def ok(path):
    os.remove(path + '/' + os.listdir(path)[0])

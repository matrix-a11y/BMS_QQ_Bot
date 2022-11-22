import os
import sys

import you_get


def download(av_BV, id):
    sys.argv = ['you-get', '-o', 'videos' + str(id) + '', "https://www.bilibili.com/video/" + av_BV]
    you_get.main()
    for i in os.listdir('videos' + str(id)):
        if (i.split('.')[-1] != 'mp4' and i.split('.')[-1] != 'flv'):
            os.remove('videos' + str(id) + '/' + i)
    return 'videos' + str(id) + '/' + os.listdir('videos' + str(id))[0]


def ok(id):
    os.remove('videos' + str(id) + '/' + os.listdir('videos' + str(id))[0])

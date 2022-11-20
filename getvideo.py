import you_get
import sys
import you_get

def download(url,path):
    sys.argv=['you-get','-o',path,url]
    you_get.main()


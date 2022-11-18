from you_get import common
def donwload(input_url):
    common.any_download(url=input_url, stream_id='mp4', info_only=False, output_dir=r'Cachedclips', merge=True)
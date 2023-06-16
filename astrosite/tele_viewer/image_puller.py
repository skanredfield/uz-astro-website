import os
import urllib.request


def pull_image_from_ftp():
    FTP_USER = os.getenv("UZSKY_FTP_USER", default="guest") 
    FTP_PASS = os.getenv("UZSKY_FTP_PASS", default="none")
    file_name = "latest_sky.png"
    remote_file_url = "ftp://{0}:{1}@example.com/ROTUZ_DATA/allskyeye/{3}".format(FTP_USER, FTP_PASS, file_name)
    local_file_path = "images/{0}".format(file_name)
    result = urllib.request.urlretrieve(remote_file_url, filename=local_file_path)

    # https://stackoverflow.com/questions/17374606/copy-file-from-template-to-static-dir
    # fd = open('%s/%s' % (settings.MEDIA_ROOT, filename), 'wb')
    #     fd.write(file['content'])
    #     fd.close()


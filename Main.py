import requests
from tqdm import tqdm
import re

def duration(sec):
    _h_ = str(sec//3600).zfill(2)
    _m_ = str((sec%3600)//60).zfill(2)
    _s_ = str((sec%3600)%60).zfill(2)
    if _h_ and _m_ == '00':
        _time_ = ("%s Seconds" % (_s_))
        return _time_
    elif _h_ == '00':
        _time_ = ("%s Minutes %s Seconds" % (_m_, _s_))
        return _time_
    else:
        _time_ = ("%s Hours %s Minutes %s Seconds" % (_h_, _m_, _s_))
        return _time_

def download(url, fname):
    strlst = r'/\:*?"<>|'
    for item in strlst:
        fname = fname.replace(item, '')
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname + '.mp4', 'wb') as file, tqdm(
            desc="$ Downloading...",
            total=total,
            ascii=r'-#',
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


id = input("\n$ YouTube Link : ")
try:
    if re.match(r'^https?://w{3}\.youtube\.com/watch\?v=(.+)$', id):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        data = {
            'q': '%s' % id,
            'vt': 'home'
        }

        info = requests.post('https://yt1s.com/api/ajaxSearch/index', headers=headers, data=data).json()
        if info['mess']:
            print("\n$ Status : %s!" % info['mess'])
        else:
            print("\n$ Title  : %s" % info['title'])
            print("$ Author : %s" % info['a'])
            print("$ Length : %i ( %s )" % (info['t'], duration(info['t'])))
            st = input("\n$ Start Time : ")
            dur = input("$ Duration : ")
            if int(st)<info['t'] and int(dur)<=(info['t']-int(st)):
                print("$ Creating.. (-%s-)" % duration(int(dur)), end='\n'*2)
                params = (
                    ('format', 'mp4'),
                    ('start', '%s' % str(int(st))),
                    ('duration', '%s' % str(int(dur))),
                    ('id', '%s' % re.search(r'^https?://w{3}\.youtube\.com/watch\?v=(.+)$', id).group(1)),
                    ('title', '%s' % info['title']),
                    ('snapshot', 'NaN')
                )
                while True:
                    response = requests.get('https://ytcutter.net/converter', params=params).json()
                    print("$ Status : %s.." % response['status'], end='\r')
                    if response['status'] == 'finished':
                        print('$ Clip : https://ytcutter.net%s' % response['watch'])
                        print('$ Direct (%.2f MB) : https://ytcutter.net/stream/%s' % (int(requests.head('https://ytcutter.net/stream/30_0s_to_14_030_0s_When_Your_Girlfriend_Undresses.mp4').headers['Content-Length'])/1024/1024, response['filename']))
                        _c_ = input('\n$ Wanna Download? (Y/N) : ').upper()
                        if _c_ == "Y":
                            download('https://ytcutter.net/stream/%s' % response['filename'], info['title'])
                        break
            else:
                print("\n$ Invalid Duration!")
    else:
        print("\n$ Invalid Link!")
except KeyboardInterrupt:
    print("\n$ KeyboardInterrupt Received!")
except ValueError:
    print("\n$ Invalid input!")

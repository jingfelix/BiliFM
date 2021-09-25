try:
    from os import system
    from json import loads
    from trans2mp3 import musicTrans
    import urllib.request
    import click

except ImportError:
    print('Module not found. Please check requirement.txt')

cli_bili = 'bilili https://www.bilibili.com/video/{0} -q {1} --danmaku no -y --disable-proxy -d {2} --audio-quality {3}'
json_url = 'https://api.bilibili.com/x/space/arc/search?mid={0}&ps=30&tid=0&pn={1}&keyword=&order=pubdate&jsonp=jsonp'
config_path = './config.json'


@click.command()
@click.option('--save', default=1, help='选择是否保存，默认为是')
@click.option('--music', default=0, help='选择是否转码为音频，默认格式为mp3，默认为否')
@click.argument('uid')
def main(save, music, uid):
    '''
    '''
    try:
        config_file = open(config_path, mode='r')
    except FileNotFoundError:
        print('config file not found!')
        return None

    config = loads(config_file.read())
    config_file.close()
    pn = int(config['BiliFM']['min-page'])
    pm = int(config['BiliFM']['max-page'])
    aq = config['Bilili']['audio-quality']
    vq = config['Bilili']['video-quality']
    di = config['Bilili']['directory']

    while pn <= pm:
        json_uid = loads(urllib.request.urlopen(
            json_url.format(uid, pn)).read())

        if json_uid['data']['list']['vlist'] == []:
            if pn == 1:
                return 'uid 错误或该用户无投稿'
            else:
                break

        for vinfo in json_uid['data']['list']['vlist']:
            system(cli_bili.format(vinfo['bvid'], vq, di, aq))
        pn += 1

    print('Video ready!')
    if music:
        musicTrans(save)

    return None


if __name__ == '__main__':
    main()

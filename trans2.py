config_path = './config.json'


def musicTrans(save: int, uid: str) -> None:
    '''transfrom mp4 file into certain format of music

    '''
    # import modules needed
    try:
        from os import walk, mkdir, path, remove # read directories
        from json import loads # load json file
        import ffmpy # use ffmpeg api
        
    except ImportError:
        print('Module not found. Please check requirement.txt')

    # open and load json file
    try:
        config_file = open(config_path, mode='r')

    except FileNotFoundError:
        print('config file not found!')
        return None

    config = loads(config_file.read())
    config_file.close()
    vd = config['Bilili']['directory']
    md = config['BiliFM']['directory']
    ft = config['BiliFM']['format']

    for curDir, dirs, files in walk(vd + uid):
        '''
        try:
            mkdir(md)
        except FileExistsError:
            pass
        '''
        
        for file in files:
            file_path = path.join(curDir, file)

            if file_path[-3:] == 'mp4':
                name = file_path.split('\\')[-1].split('.')[0]
                music_path = '{0}/{1}.{2}'.format(md, name, ft)

                if not path.exists(music_path):
                    ff = ffmpy.FFmpeg(
                        inputs={file_path: None},
                        outputs={music_path: None}
                    )
                    ff.run()

                else:
                    print('{0}.{1} exists, jump to next one!\n'.format(name, ft))
                
                if not save:
                    remove(file_path)

            elif file_path[-3:] == 'dpl':
                remove(file_path)

    print('Music ready!')

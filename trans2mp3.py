def musicTrans(save: int) -> None:
    '''
    '''
    try:
        from os import walk, mkdir, path, remove
        import ffmpy
    except ImportError:
        print('Module not found. Please check requirement.txt')

    for curDir, dirs, files in walk('.'):
        try:
            mkdir('music')
        except FileExistsError:
            pass
        for file in files:
            file_path = path.join(curDir, file)
            if file_path[-3:] == 'mp4':
                name = file_path.split('\\')[-1].split('.')[0]
                ff = ffmpy.FFmpeg(
                    inputs={file_path: None},
                    outputs={'./music/{0}.mp3'.format(name): None}
                )
                ff.run()
                if not save:
                    remove(file_path)
            elif file_path[-3:] == 'dpl':
                remove(file_path)

    print('Music ready!')

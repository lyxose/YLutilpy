def random_name(path=None,head='',end='') -> str:
    '''
    return a temporal file name that will not conflict with existing files 
    this function will try coding the temporal file by insert the real time 
    if failed, then try a random int seq
    
    path: the target folder path (if None, the path will be the working path)
    head: the specified file name prefix
    end: the specified file name suffix
    '''
    import os
    import random
    from datetime import datetime
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'{head}_temp_{now}_{end}'
    while filename in os.listdir(path):
        filename = f'temp_{random.randint(100000,10000000)}'
    return filename

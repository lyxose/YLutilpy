def evenly_split(data,n_group:int,ReturnType='index') -> list:  
    '''
    devide a int / list / ndarray to groups with min difference (0 or 1)
    the larger group will be set to the two tails
    -------------
    e.g. 
    data = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    index = evenly_split(data,5) -> index = [0,3,5,7,10,13] 
    *recommended usage1:*
    for i in range(len(index)-1): data[index[i]:index[i+1]]...
    *recommended usage2:*
    for this_split in np.split(data,index[1:-1],axis=0): 
    ''' 
    import numpy as np
    import math
    index = [0]
    num = []
    if type(data)==list:
        data = len(data)
    if type(data)==np.ndarray:
        data = data.shape[0]
    if type(data)==int:
        if data<n_group:raise ValueError('Invalid number: n_group should not be larger than data (or its length)')
        r = data%n_group    # remainder
        n = data//n_group   # average number
        for i in range(n_group):  
            if i < r//2 or i>=n_group-math.ceil(r/2): # set larger groups at two tails
                index.append(index[-1]+n+1)
                num.append(n+1)
            else: 
                index.append(index[-1]+n)
                num.append(n)
    else: raise TypeError('data should be an int / list / ndarray')
    return index if ReturnType=='index' else num

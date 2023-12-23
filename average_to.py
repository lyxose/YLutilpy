import numpy as np
def average_to(data:np.ndarray, n_group:int, dim=0):
    '''
    to equally (as far as possible) devide data to n_group and average at this specified dimension.
    
    data: the np.ndarray to group and average
    n_group: the group count to devide
    dim: the dim to average across

    if data shapes (10,9,8), n_group=3, dim=2
    return: the averaged data shapes (10,9,3)
    '''
    from utility.evenly_split import evenly_split
    # print(f"data.shape = {data.shape}")
    index = evenly_split(data.shape[dim],n_group)  # split index
    averaged_data=[]
    for this_split in np.split(data,index[1:-1],axis=dim): 
        averaged_data.append(this_split.mean(axis=dim))
    # reshape the data (transpose the axis)
    dim_index = [i for i in range(1,len(data.shape)) ]
    dim_index.insert(dim,0)
    averaged_data = np.transpose(np.array(averaged_data),dim_index)
    # print(f"averaged_data.shape = {averaged_data.shape}")
    return averaged_data

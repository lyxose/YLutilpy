from typing import Optional
import os
import pickle
import shutil

class figdata:

    # naxs = 0
    # var_dicts=[]  # list of dicts that store the variables
    # def __init__(self) -> None:
    #     pass

    def __init__(self, var_names:Optional[str] , *variables) -> None:
        '''
        var_names: str, the names of variables separated by comma (like "var1, var2, var3...", just copy the *variables parameters and paste them in qoutes)
        *variables: the variables in the order of var_names
        '''
        self.naxs = 0
        self.var_dicts = []
        self.desc_dicts = []
        if var_names is not None:
            self.add_ax(var_names, *variables)

    def add_ax(self,var_names:str|None, *variables, descriptions=[]) -> None:
        '''
        var_names: str, the names of variables separated by comma (like "var1, var2, var3...", just copy the *variables parameters and paste them in qoutes)
        *variables: the variables in the order of var_names
        descriptions: list of None|str, to describe the variables orderly  
        '''
        self.var_dicts.append({})
        self.desc_dicts.append({})
        self.naxs += 1
        if var_names is not None:
            self.add_vars(var_names,*variables,axn = None,descriptions = descriptions)
    
    def add_vars(self,  var_names:str, *variables, axn:int=None,descriptions=[]) -> None:
        '''
        var_names: str, the names of variables separated by comma (like "var1, var2, var3...", just copy the *variables parameters and paste them in qoutes)
        *variables: the variables in the order of var_names
        axn: int | none (default), index of ax to add variables (if none, default as the latest added ax)
        descriptions: list of None|str, to describe the variables orderly  
        '''
        if axn is None:
            axn=len(self.var_dicts)-1
        var_names = var_names.split(',')
        if len(var_names)!=len(variables): 
            raise ValueError(f'The number of var_names ({len(var_names)}) is inconsistent with *variables ({len(variables)})')
        for i in range(len(variables)-len(descriptions)):
            descriptions.append(None)
        for name,var,descriptions in zip(var_names,variables,descriptions):
            name=name.strip()  # remove the space 
            if name in self.var_dicts[axn].keys(): raise ValueError(f'{name} variable is already in dicts of ax{axn}')  # 暂不考虑覆写需求
            if ' ' in name: raise ValueError('The var_names should not contain any space')
            self.var_dicts[axn][name]=var
            self.desc_dicts[axn][name]=descriptions


    def save_figdata(self, fpath:str, intro_script=True, script_name='defaulted_datareader', data_name='data.pkl', rewrite=False):
        '''
        fig_data: dict | list of dict, the key should be the name of the variable
        fpath: str, folder path to save figdata
        intro_script: the python script to read the data
        script_name: the filename of that python script 

        output: 
            fpath/fig_data.pkl      -> the fig_data object
            fpath/{script_name}.py  -> the default script to read the fig_data.pkl data 
        '''

        fig_data = self.var_dicts
        fig_data.append(self.desc_dicts)  # last object is desc_dicts
        if not os.path.exists(fpath):   
            os.makedirs(fpath)
        if os.path.exists(f'{fpath}/data.pkl') and not rewrite:
            raise FileExistsError(f'{fpath}/data.pkl already exists!!!')
        with open(f'{fpath}/data.pkl','wb+') as f:
            pickle.dump(fig_data,f,protocol=3)  # python>=3
        if intro_script:    
            if os.path.exists(f'{fpath}/default_img_set.py') and not rewrite:
                raise FileExistsError(f'{fpath}/default_img_set.py already exists!!!')
            shutil.copy(f'{os.path.dirname(__file__)}/default_img_set.py',fpath)
            with open(f'{fpath}/{script_name}.py','w+') as f:
                head = \
f'''# %%
import pickle 
import numpy as np
import matplotlib.pyplot as plt
from default_img_set import default_img_set 

default_img_set()
with open('./{data_name}','rb') as f:
    data = pickle.load(f)
'''
                f.write(head)
                if len(fig_data)-1!=1:
                    fig_setting = \
f'''# %%
ncols = 2
nrows =  round(np.ceil({len(fig_data)-1}/ncols))
fig,axs = plt.subplots(nrows,ncols,dpi=300,figsize=(ncols*4,nrows*4))
# axs = np.transpose(axs,[1,0])  # use this to change the plot order
axs = np.reshape(axs,-1)  
'''
                    f.write(fig_setting+f'for axn in range({len(fig_data)-1}):\n')
                    shared_vars = set(fig_data[0].keys())  #  variables shared by all of the subplots
                    for axn in range(1,len(fig_data)-1):
                        shared_vars = shared_vars.intersection(fig_data[axn].keys())
                    for var in shared_vars:
                        f.write(f'    {var} = data[axn]["{var}"]')
                        desc = self.desc_dicts[axn][var] 
                        while desc is None and axn>=0:
                            axn-=1
                            desc = self.desc_dicts[axn][var] # use the last description for the shared variables
                        f.write(f'{f"# {desc}"if desc is not None else ""} \n') 
                    for axn in range(len(fig_data)-1):  # unique variables 
                        special_vars = set(fig_data[axn].keys()).difference(shared_vars)
                        if len(special_vars)>0: 
                            f.write(f'    if axn=={axn}:\n')
                            for var in special_vars:
                                f.write(f'        {var} = data[axn]["{var}"]')
                                desc = self.desc_dicts[axn][var]
                                f.write(f'{f"  # {desc}"if desc is not None else ""} \n') 
                else:
                    f.write(\
f'''# %%
fig,ax = plt.subplots(1,dpi=300,figsize=(5,4))
''')
                    for var in fig_data[0].keys():
                        f.write(f'{var} = data[0]["{var}"]')
                        f.write(f'# {self.desc_dicts[0][var]}\n')
                figname = os.path.basename(fpath)
                f.write(f'\n\n# %% \nfig.savefig("{figname}.pdf")')    

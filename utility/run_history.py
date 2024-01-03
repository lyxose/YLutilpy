# %% 
from datetime import datetime
import sys
import os.path as op
from os import makedirs
import pickle
# %% 

class history:
    '''
    An automatic script and variable history storage module 

    - Use the `save_script(path)` to save the original script to 
      'path/<time>_<scriptname>.py' (data output path is suggested)

    - Use the `save_vars(locals(), path)` to save the variables to
      'path/<time>_<scriptname>.pkl' at any stage of main program

    '''

    def __init__(self) -> None:
        '''
        Automatically save:
        - path: the path of original script file
        - script_name: the file name of original script
        - script: the script content
        - start_time: the time of saving above (instantiation time)
        '''
        self.path = sys.argv[0]  # path of original script
        self.script_name = op.basename(self.path)
        with open(self.path,'r') as f:
            self.script = f.read()
        self.start_time = datetime.now()
    
    def save_script(self,path=None,name=None) -> None:
        if path is None:
            path = op.dirname(self.path)
        if name is None:
            name = datetime.now().strftime('%Y%m%d_%H%M%S_') + self.script_name
        if not op.exists(path): 
            makedirs(path)
        self.script_save_path = op.join(path,name)
        with open(self.script_save_path,'w+') as f:
            f.write(f'# Started at: {self.start_time}')
            f.write(self.script)

    def save_vars(self,vars:dict,path=None,name=None) -> None:
        '''
        vars: the name-value dicts of variables to store
        ** use `vars=locals()` to save all variables that supported
        '''
        self.var_save_time = datetime.now()
        vars['var_save_time']=self.var_save_time
        if path is None:
            path = op.dirname(self.path)
        if name is None:
            name = self.var_save_time.strftime('%Y%m%d_%H%M%S_') + self.script_name[:-3] + '.pkl'
        if not op.exists(path): 
            makedirs(path)
        self.var_save_path = op.join(path,name)
        with open(self.var_save_path,'wb+') as f:
            for k,v in vars.copy().items():
                try:
                    pickle.dump({k:v}, f, protocol=3)  # python >= 3
                except (AttributeError,TypeError) as e:
                    print(e)
                    print(f'{k}:{v} is not saved\n') 
                    del vars[k]
        with open(self.var_save_path,'wb+') as f:
            pickle.dump(vars, f, protocol=3)  # python >= 3
        self.vars = vars
        if hasattr(self,'script_save_path'):
            relative_path = op.relpath(self.var_save_path,op.dirname(self.script_save_path))
            with open(self.script_save_path, 'r+') as f:
                content = f.read()
                f.seek(0)  # make the pointer the head of the file
                f.write(
f'''
# %%
import pickle
with open(r'{relative_path}','rb') as f:
    vars_history = pickle.load(f)
# %% 
''')
                f.write(content)



    
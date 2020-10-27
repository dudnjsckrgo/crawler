# 프로퍼티 url, parser , path, api, apikey 전부 str 타입
from dataclasses import dataclass

@dataclass
class Entity:
    url :str = ''
    filename=''
    parser : str = ''
    path: str = ''
    api : str = ''
    apikey : str = ''
    dict : object =None
    columns :object =None
    new_folder_name :str =''
    tag :str =''
    attrs :str=''
    replace_str: str =''
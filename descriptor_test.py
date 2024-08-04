from pathlib import Path

# from pathlib import Path

class PathConversionDescriptor:
    
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f'_{name}'
        
    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.private_name)
        return value
    
    def __set__(self, obj, value):
        match value:
            case str():
                setattr(obj, self.private_name, Path(value))
            case Path():
                setattr(obj, self.private_name, value)
            case _:
                raise ValueError(f'Cannot convert {value!s} to pathlib.Path')


pcd = Path('webern_lieder_02.png')

from dataclasses import dataclass
@dataclass
class FileHolder:
    held_file: PathConversionDescriptor = PathConversionDescriptor()
    

fh = FileHolder(held_file='webern_lieder_02.png')
print(fh)
print(fh.held_file)
# OUT: 'webern_lieder_02.png'
print(type(fh.held_file))
# OUT: <class 'str'>
###  
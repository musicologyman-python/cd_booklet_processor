from collections.abc import Iterable
from dataclasses import dataclass, field
from functools import partial
import json
from pathlib import Path
import re
from typing import NamedTuple

FILE_NAME_RE = re.compile(r'(\.\/)?(?P<base_name>\w+)_+'
                          r'(?P<page_number>\d+)(?=\.\w+)')

class ParsedFileName(NamedTuple):
    base_name: str
    page_number: int


def parse_file_name(filename: str):
    match FILE_NAME_RE.search(filename):
        case re.Match() as m:
            return ParsedFileName(**m.groupdict())

def get_page_number_from_file(file: str|Path) -> int:
    match file:
        case str():
            return get_page_number_from_file(Path(file))
        case Path():
            filename: str = file.name
    match FILE_NAME_RE.search(filename):
        case re.Match() as m:
            return int(m[0])


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


@dataclass
class ImageInfo():

    __DEST_DIR_NAME = 'split_pages'

    file: PathConversionDescriptor = PathConversionDescriptor()
    width: int
    height: int
    original_page_number: int
    left_page_number: int
    right_page_number: int
    left_crop_geometry: str = field(init=False)
    right_crop_geometry: str = field(init=False)
    parsed_file_name: ParsedFileName = field(init=False)
    dest_dir: Path = field(init=False)
    left_page_file: Path = field(init=False)
    right_page_file: Path = field(init=False)

    def __get_dest_dir(self) -> Path:
        dest_dir: Path = self.file.parent / self.__class__.__DEST_DIR_NAME
        dest_dir.mkdir(exist_ok=True)
        return dest_dir

    def __post_init__(self):
        half_width = self.width // 2
        self.left_crop_geometry = \
            f'{half_width}x{self.height}+0x0'
        self.right_crop_geometry = \
            f'{half_width + self.width % 2}x{self.height}' \
            f'+{half_width + self.width % 2}x0'
        self.parsed_file_name = parse_file_name(self.file.name)
        self.dest_dir = self.__get_dest_dir()
        self.left_page_file = (self.dest_dir / 
                               f'{self.parsed_file_name.base_name}_'
                               f'{self.left_page_number:02}{self.file.suffix}')
        self.right_page_file = (self.dest_dir / 
                               f'{self.parsed_file_name.base_name}_'
                               f'{self.right_page_number:02}{self.file.suffix}')

def get_left_crop_command(info: ImageInfo) -> str:
    return f'magick {info.file!s} -crop {info.left_crop_geometry} ' \
           f'{info.left_page_file}'

def get_right_crop_command(info: ImageInfo) -> str:
    return f'magick {info.file!s} -crop {info.right_crop_geometry} ' \
           f'{info.right_page_file}'

def read_json_file(filename: str='resize_info.json') -> dict:
    with open(filename) as fp:
        return json.load(fp)

def get_infos(infos: list[dict]) -> Iterable:
    yield from (ImageInfo(**info) for info in infos)

def main():
    infos = read_json_file() 
    crop_commands = Path('crop_commands.sh')
    with crop_commands.open(mode='w') as fp:

        printf = partial(print, file=fp)
        printf('#!/bin/bash')

        for info in get_infos(infos):
            printf(get_left_crop_command(info))
            printf(get_right_crop_command(info))

    crop_commands.chmod(0o777)

if __name__ == '__main__':
    main()
from crop_command_maker import ImageInfo
import dataclasses
import json
from pprint import pprint
with open('resize_info.json') as fp:
    resize_info = json.load(fp)
    

info = ImageInfo(**resize_info[0])
pprint(dataclasses.asdict(info))
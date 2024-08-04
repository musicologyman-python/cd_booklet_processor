import csv
from functools import partial
import operator
from pathlib import Path
from pprint import pprint

from lxml import etree
import regex
from toolz import curried
from toolz.functoolz import compose_left, curry, pipe

def read_all_lines(filename: str) -> list[str]:
    return Path(filename).read_text().splitlines()

def get_files(parent: Path=Path.cwd(), filter=lambda p:True) -> list[Path]:
    return pipe(parent.iterdir(), 
                curried.filter(filter), 
                curried.map(lambda p: p.relative_to(parent)),
                sorted, 
                list)

def printl(l: list) -> None:
    for item in l:
        print(f'{item!s}')

def read_csv(filename: str, enc: str='utf-8') -> list:
    with open(filename, mode='r', encoding=enc, newline='') as fp:
        reader = csv.DictReader(fp)
        return [row for row in reader]


resize_info = read_csv('resize_info.csv')
pprint(resize_info)
# OUT: [{'file': './webern_lieder_02.png', 'height': '1319 ', 'width': '2755'},
# OUT:  {'file': './webern_lieder_03.png', 'height': '1361 ', 'width': '2768'},
# OUT:  {'file': './webern_lieder_04.png', 'height': '1347 ', 'width': '2760'},
# OUT:  {'file': './webern_lieder_05.png', 'height': '1416 ', 'width': '2836'},
# OUT:  {'file': './webern_lieder_06.png', 'height': '1385 ', 'width': '2826'},
# OUT:  {'file': './webern_lieder_07.png', 'height': '1400 ', 'width': '2776'},
# OUT:  {'file': './webern_lieder_08.png', 'height': '1416 ', 'width': '2836'},
# OUT:  {'file': './webern_lieder_09.png', 'height': '1351 ', 'width': '2762'},
# OUT:  {'file': './webern_lieder_10.png', 'height': '1395 ', 'width': '2770'},
# OUT:  {'file': './webern_lieder_11.png', 'height': '1408 ', 'width': '2820'},
# OUT:  {'file': './webern_lieder_12.png', 'height': '1416 ', 'width': '2812'},
# OUT:  {'file': './webern_lieder_13.png', 'height': '1416 ', 'width': '2844'},
# OUT:  {'file': './webern_lieder_14.png', 'height': '1412 ', 'width': '2832'},
# OUT:  {'file': './webern_lieder_15.png', 'height': '1412 ', 'width': '2820'},
# OUT:  {'file': './webern_lieder_16.png', 'height': '1420 ', 'width': '2824'},
# OUT:  {'file': './webern_lieder_17.png', 'height': '1412 ', 'width': '2828'},
# OUT:  {'file': './webern_lieder_18.png', 'height': '1420 ', 'width': '2824'},
# OUT:  {'file': './webern_lieder_19.png', 'height': '1420 ', 'width': '2828'},
# OUT:  {'file': './webern_lieder_20.png', 'height': '1412 ', 'width': '2852'},
# OUT:  {'file': './webern_lieder_21.png', 'height': '1416 ', 'width': '2820'},
# OUT:  {'file': './webern_lieder_22.png', 'height': '1420 ', 'width': '2824'}]
for row in resize_info:
    row['height'] = int(row['height'])
    row['width'] = int(row['width'])
    

pprint(resize_info)
# OUT: [{'file': './webern_lieder_02.png', 'height': 1319, 'width': 2755},
# OUT:  {'file': './webern_lieder_03.png', 'height': 1361, 'width': 2768},
# OUT:  {'file': './webern_lieder_04.png', 'height': 1347, 'width': 2760},
# OUT:  {'file': './webern_lieder_05.png', 'height': 1416, 'width': 2836},
# OUT:  {'file': './webern_lieder_06.png', 'height': 1385, 'width': 2826},
# OUT:  {'file': './webern_lieder_07.png', 'height': 1400, 'width': 2776},
# OUT:  {'file': './webern_lieder_08.png', 'height': 1416, 'width': 2836},
# OUT:  {'file': './webern_lieder_09.png', 'height': 1351, 'width': 2762},
# OUT:  {'file': './webern_lieder_10.png', 'height': 1395, 'width': 2770},
# OUT:  {'file': './webern_lieder_11.png', 'height': 1408, 'width': 2820},
# OUT:  {'file': './webern_lieder_12.png', 'height': 1416, 'width': 2812},
# OUT:  {'file': './webern_lieder_13.png', 'height': 1416, 'width': 2844},
# OUT:  {'file': './webern_lieder_14.png', 'height': 1412, 'width': 2832},
# OUT:  {'file': './webern_lieder_15.png', 'height': 1412, 'width': 2820},
# OUT:  {'file': './webern_lieder_16.png', 'height': 1420, 'width': 2824},
# OUT:  {'file': './webern_lieder_17.png', 'height': 1412, 'width': 2828},
# OUT:  {'file': './webern_lieder_18.png', 'height': 1420, 'width': 2824},
# OUT:  {'file': './webern_lieder_19.png', 'height': 1420, 'width': 2828},
# OUT:  {'file': './webern_lieder_20.png', 'height': 1412, 'width': 2852},
# OUT:  {'file': './webern_lieder_21.png', 'height': 1416, 'width': 2820},
# OUT:  {'file': './webern_lieder_22.png', 'height': 1420, 'width': 2824}]
import re
ORIG_PAGE_NUM_RE = re.compile(r'(?<=webern_lieder_)\d+(?=\.png)')
def extract_page_number(filename):
    m = ORIG_PAGE_NUM_RE.search(filename)
    return int(m[0])

for row in resize_info:
    print(f'{row["file"]} -> {extract_page_number(row["file"])}')
    

# OUT: ./webern_lieder_02.png -> 2
# OUT: ./webern_lieder_03.png -> 3
# OUT: ./webern_lieder_04.png -> 4
# OUT: ./webern_lieder_05.png -> 5
# OUT: ./webern_lieder_06.png -> 6
# OUT: ./webern_lieder_07.png -> 7
# OUT: ./webern_lieder_08.png -> 8
# OUT: ./webern_lieder_09.png -> 9
# OUT: ./webern_lieder_10.png -> 10
# OUT: ./webern_lieder_11.png -> 11
# OUT: ./webern_lieder_12.png -> 12
# OUT: ./webern_lieder_13.png -> 13
# OUT: ./webern_lieder_14.png -> 14
# OUT: ./webern_lieder_15.png -> 15
# OUT: ./webern_lieder_16.png -> 16
# OUT: ./webern_lieder_17.png -> 17
# OUT: ./webern_lieder_18.png -> 18
# OUT: ./webern_lieder_19.png -> 19
# OUT: ./webern_lieder_20.png -> 20
# OUT: ./webern_lieder_21.png -> 21
# OUT: ./webern_lieder_22.png -> 22
def get_left_page_number(double_page_number):
    return (double_page_number - 1) * 2

def get_right_page_number(double_page_number):
    return get_left_page_number(double_page_number) + 1


for row in resize_info:
    row['original_page_number'] = extract_page_number(row['file'])
    

pprint(resize_info)
# OUT: [{'file': './webern_lieder_02.png',
# OUT:   'height': 1319,
# OUT:   'original_page_number': 2,
# OUT:   'width': 2755},
# OUT:  {'file': './webern_lieder_03.png',
# OUT:   'height': 1361,
# OUT:   'original_page_number': 3,
# OUT:   'width': 2768},
# OUT:  {'file': './webern_lieder_04.png',
# OUT:   'height': 1347,
# OUT:   'original_page_number': 4,
# OUT:   'width': 2760},
# OUT:  {'file': './webern_lieder_05.png',
# OUT:   'height': 1416,
# OUT:   'original_page_number': 5,
# OUT:   'width': 2836},
# OUT:  {'file': './webern_lieder_06.png',
# OUT:   'height': 1385,
# OUT:   'original_page_number': 6,
# OUT:   'width': 2826},
# OUT:  {'file': './webern_lieder_07.png',
# OUT:   'height': 1400,
# OUT:   'original_page_number': 7,
# OUT:   'width': 2776},
# OUT:  {'file': './webern_lieder_08.png',
# OUT:   'height': 1416,
# OUT:   'original_page_number': 8,
# OUT:   'width': 2836},
# OUT:  {'file': './webern_lieder_09.png',
# OUT:   'height': 1351,
# OUT:   'original_page_number': 9,
# OUT:   'width': 2762},
# OUT:  {'file': './webern_lieder_10.png',
# OUT:   'height': 1395,
# OUT:   'original_page_number': 10,
# OUT:   'width': 2770},
# OUT:  {'file': './webern_lieder_11.png',
# OUT:   'height': 1408,
# OUT:   'original_page_number': 11,
# OUT:   'width': 2820},
# OUT:  {'file': './webern_lieder_12.png',
# OUT:   'height': 1416,
# OUT:   'original_page_number': 12,
# OUT:   'width': 2812},
# OUT:  {'file': './webern_lieder_13.png',
# OUT:   'height': 1416,
# OUT:   'original_page_number': 13,
# OUT:   'width': 2844},
# OUT:  {'file': './webern_lieder_14.png',
# OUT:   'height': 1412,
# OUT:   'original_page_number': 14,
# OUT:   'width': 2832},
# OUT:  {'file': './webern_lieder_15.png',
# OUT:   'height': 1412,
# OUT:   'original_page_number': 15,
# OUT:   'width': 2820},
# OUT:  {'file': './webern_lieder_16.png',
# OUT:   'height': 1420,
# OUT:   'original_page_number': 16,
# OUT:   'width': 2824},
# OUT:  {'file': './webern_lieder_17.png',
# OUT:   'height': 1412,
# OUT:   'original_page_number': 17,
# OUT:   'width': 2828},
# OUT:  {'file': './webern_lieder_18.png',
# OUT:   'height': 1420,
# OUT:   'original_page_number': 18,
# OUT:   'width': 2824},
# OUT:  {'file': './webern_lieder_19.png',
# OUT:   'height': 1420,
# OUT:   'original_page_number': 19,
# OUT:   'width': 2828},
# OUT:  {'file': './webern_lieder_20.png',
# OUT:   'height': 1412,
# OUT:   'original_page_number': 20,
# OUT:   'width': 2852},
# OUT:  {'file': './webern_lieder_21.png',
# OUT:   'height': 1416,
# OUT:   'original_page_number': 21,
# OUT:   'width': 2820},
# OUT:  {'file': './webern_lieder_22.png',
# OUT:   'height': 1420,
# OUT:   'original_page_number': 22,
# OUT:   'width': 2824}]
for row in resize_info:
    row['left_page_number'] = get_left_page_number(row['original_page_number'])
    row['right_page_number'] = get_right_page_number(row['original_page_number'])
    

pprint(resize_info)
# OUT: [{'file': './webern_lieder_02.png',
# OUT:   'height': 1319,
# OUT:   'left_page_number': 2,
# OUT:   'original_page_number': 2,
# OUT:   'right_page_number': 3,
# OUT:   'width': 2755},
# OUT:  {'file': './webern_lieder_03.png',
# OUT:   'height': 1361,
# OUT:   'left_page_number': 4,
# OUT:   'original_page_number': 3,
# OUT:   'right_page_number': 5,
# OUT:   'width': 2768},
# OUT:  {'file': './webern_lieder_04.png',
# OUT:   'height': 1347,
# OUT:   'left_page_number': 6,
# OUT:   'original_page_number': 4,
# OUT:   'right_page_number': 7,
# OUT:   'width': 2760},
# OUT:  {'file': './webern_lieder_05.png',
# OUT:   'height': 1416,
# OUT:   'left_page_number': 8,
# OUT:   'original_page_number': 5,
# OUT:   'right_page_number': 9,
# OUT:   'width': 2836},
# OUT:  {'file': './webern_lieder_06.png',
# OUT:   'height': 1385,
# OUT:   'left_page_number': 10,
# OUT:   'original_page_number': 6,
# OUT:   'right_page_number': 11,
# OUT:   'width': 2826},
# OUT:  {'file': './webern_lieder_07.png',
# OUT:   'height': 1400,
# OUT:   'left_page_number': 12,
# OUT:   'original_page_number': 7,
# OUT:   'right_page_number': 13,
# OUT:   'width': 2776},
# OUT:  {'file': './webern_lieder_08.png',
# OUT:   'height': 1416,
# OUT:   'left_page_number': 14,
# OUT:   'original_page_number': 8,
# OUT:   'right_page_number': 15,
# OUT:   'width': 2836},
# OUT:  {'file': './webern_lieder_09.png',
# OUT:   'height': 1351,
# OUT:   'left_page_number': 16,
# OUT:   'original_page_number': 9,
# OUT:   'right_page_number': 17,
# OUT:   'width': 2762},
# OUT:  {'file': './webern_lieder_10.png',
# OUT:   'height': 1395,
# OUT:   'left_page_number': 18,
# OUT:   'original_page_number': 10,
# OUT:   'right_page_number': 19,
# OUT:   'width': 2770},
# OUT:  {'file': './webern_lieder_11.png',
# OUT:   'height': 1408,
# OUT:   'left_page_number': 20,
# OUT:   'original_page_number': 11,
# OUT:   'right_page_number': 21,
# OUT:   'width': 2820},
# OUT:  {'file': './webern_lieder_12.png',
# OUT:   'height': 1416,
# OUT:   'left_page_number': 22,
# OUT:   'original_page_number': 12,
# OUT:   'right_page_number': 23,
# OUT:   'width': 2812},
# OUT:  {'file': './webern_lieder_13.png',
# OUT:   'height': 1416,
# OUT:   'left_page_number': 24,
# OUT:   'original_page_number': 13,
# OUT:   'right_page_number': 25,
# OUT:   'width': 2844},
# OUT:  {'file': './webern_lieder_14.png',
# OUT:   'height': 1412,
# OUT:   'left_page_number': 26,
# OUT:   'original_page_number': 14,
# OUT:   'right_page_number': 27,
# OUT:   'width': 2832},
# OUT:  {'file': './webern_lieder_15.png',
# OUT:   'height': 1412,
# OUT:   'left_page_number': 28,
# OUT:   'original_page_number': 15,
# OUT:   'right_page_number': 29,
# OUT:   'width': 2820},
# OUT:  {'file': './webern_lieder_16.png',
# OUT:   'height': 1420,
# OUT:   'left_page_number': 30,
# OUT:   'original_page_number': 16,
# OUT:   'right_page_number': 31,
# OUT:   'width': 2824},
# OUT:  {'file': './webern_lieder_17.png',
# OUT:   'height': 1412,
# OUT:   'left_page_number': 32,
# OUT:   'original_page_number': 17,
# OUT:   'right_page_number': 33,
# OUT:   'width': 2828},
# OUT:  {'file': './webern_lieder_18.png',
# OUT:   'height': 1420,
# OUT:   'left_page_number': 34,
# OUT:   'original_page_number': 18,
# OUT:   'right_page_number': 35,
# OUT:   'width': 2824},
# OUT:  {'file': './webern_lieder_19.png',
# OUT:   'height': 1420,
# OUT:   'left_page_number': 36,
# OUT:   'original_page_number': 19,
# OUT:   'right_page_number': 37,
# OUT:   'width': 2828},
# OUT:  {'file': './webern_lieder_20.png',
# OUT:   'height': 1412,
# OUT:   'left_page_number': 38,
# OUT:   'original_page_number': 20,
# OUT:   'right_page_number': 39,
# OUT:   'width': 2852},
# OUT:  {'file': './webern_lieder_21.png',
# OUT:   'height': 1416,
# OUT:   'left_page_number': 40,
# OUT:   'original_page_number': 21,
# OUT:   'right_page_number': 41,
# OUT:   'width': 2820},
# OUT:  {'file': './webern_lieder_22.png',
# OUT:   'height': 1420,
# OUT:   'left_page_number': 42,
# OUT:   'original_page_number': 22,
# OUT:   'right_page_number': 43,
# OUT:   'width': 2824}]
import json
with open('resize_info.json', mode='w') as fp:
    json.dump(resize_info, fp, indent=2)
    

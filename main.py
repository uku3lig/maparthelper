import pandas as pd
import argparse
import math
import sys

from typing import Dict, List


PRIMARY_DYES = ["Black", "Blue", "Brown", "Green", "Red", "White", "Yellow"]
QUASI_PRIMARY_DYES = ["Light Blue", "Light Gray", "Lime", "Magenta", "Orange", "Pink"]


def print_item(name: str, padding: int, count: int) -> None:
    s = f'{name:<{padding}}  '

    if args.p == 'shulker' and (args.strict or (count < 1728 and not args.l) or count >= 1728):
        s += f"{(n := math.ceil(count / 1728))} shulker{'s' if n > 1 else ''}"
        count = 0
    elif count >= 1728 and not args.strict:
        s += f"{(n := count // 1728)} shulker{'s' if n > 1 else ''} "
        count %= 1728
    
    if args.p == 'stack' and (args.strict or (count < 64 and not args.l) or count >= 64):
        s += f"{(n := math.ceil(count / 64))} stack{'s' if n > 1 else ''}"
        count = 0
    elif count >= 64 and not args.strict:
        s += f"{(n := count // 64)} stack{'s' if n > 1 else ''} "
        count %= 64

    if count != 0:
        s += f"{count} item{'s' if count > 1 else ''}"

    print(s)

def get_dyes(items: Dict[str, int], type: str) -> Dict[str, int]:
    dyes = {n[:-11]: math.ceil(a / 8) for n, a in items.items() if "Terracotta" in n}
    if type == 'quasi' or type == 'primary':
        print('WARNING: You should also print the list of all dyes to know how many to craft')
        for n in list(dyes):
            if n in PRIMARY_DYES or n in QUASI_PRIMARY_DYES:
                continue

            c = math.ceil(dyes.pop(n) / 2)

            if n == 'Cyan':
                add(dyes, ['Green', 'Blue'], c)
            elif n == 'Gray':
                add(dyes, ['Black', 'White'], c)
            elif n == 'Purple':
                add(dyes, ['Red', 'Blue'], c)

    if type == 'primary':
        for n in list(dyes):
            if n in PRIMARY_DYES:
                continue
            
            if n == 'Light Gray':
                c = math.ceil(dyes.pop(n) / 3)
            elif n == 'Magenta':
                c = math.ceil(dyes.pop(n) / 4)
            else:
                c = math.ceil(dyes.pop(n) / 2)
            
            if n == 'Light Blue':
                add(dyes, ['Blue', 'White'], c)
            elif n == 'Light Gray':
                add(dyes, ['Black'], c)
                add(dyes, ['White'], c * 2)
            elif n == 'Lime':
                add(dyes, ['Green', 'White'], c)
            elif n == 'Magenta':
                add(dyes, ['Blue', 'White'], c)
                add(dyes, ['Red'], c * 2)
            elif n == 'Orange':
                add(dyes, ['Red', 'Yellow'], c)
            elif n == 'Pink':
                add(dyes, ['Red', 'White'], c)

    return dict(sorted(dyes.items(), key=lambda item: item[1], reverse=True))

def add(d: Dict[str, int], keys: List[str], amount: int) -> None:
    for e in keys:
        d[e] = d.get(e, 0) + amount


parser = argparse.ArgumentParser()
parser.add_argument('file', help='path to the csv file containing the material list')
parser.add_argument('-p', choices=['shulker', 'stack', 'item'], default='stack', help='lowest precision of the values')
parser.add_argument('-l', help='if values are lower than the precision, display them more precisely', action='store_true')
parser.add_argument('--strict', help='keep all values in the defined precision', action='store_true')
parser.add_argument('--dye', '-d', help='compute the amount of dye needed', choices=['all', 'quasi', 'primary'], default=None)

args = parser.parse_args()

if args.l and args.strict:
    print("-l and --strict are mutually exclusive. Exiting.")
    sys.exit()

data = pd.read_csv(args.file, usecols=['Item', 'Total'], index_col=0).squeeze('columns').to_dict()

if args.dye is not None:
    data = get_dyes(data, args.dye)

longest = len(max(data.keys(), key=len))
for name, count in data.items():
    print_item(name, longest, count)
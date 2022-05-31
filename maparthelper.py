import argparse
import csv
import math
import sys

from typing import Dict, List


PRIMARY_DYES = ["Black", "Blue", "Brown", "Green", "Red", "White", "Yellow"]
QUASI_PRIMARY_DYES = ["Light Blue", "Light Gray", "Lime", "Magenta", "Orange", "Pink"]
TALL_FLOWERS = ["Red", "Pink", "Magenta", "Yellow"]
TALL_FLOWER_CRAFTABLE = ["Orange", "Purple"]


def print_item(name: str, padding: int, count: int) -> None:
    s = f'{name:<{padding}} '

    if args.precision == 'shulker' and (args.strict or (count < 1728 and not args.lower) or count >= 1728):
        s += f"{(n := math.ceil(count / 1728))} shulker{'s' if n > 1 else ''}"
        count = 0
    elif count >= 1728 and not args.strict:
        s += f"{(n := count // 1728)} shulker{'s' if n > 1 else ''} "
        count %= 1728
    
    if args.precision == 'stack' and (args.strict or (count < 64 and not args.lower) or count >= 64):
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

    if type == 'tall':
        for n in list(dyes):
            if n not in TALL_FLOWER_CRAFTABLE:
                continue
            c = math.ceil(dyes.pop(n) / 2)
            add(dyes, ['Red', 'Yellow' if n == 'Orange' else 'Blue'], c)

        dyes = {n: math.ceil(a / 2) for n, a in dyes.items() if n in TALL_FLOWERS}


    if type == 'quasi' or 'prim' in type:
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

    if 'prim' in type:
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
            elif n == 'Magenta' and type == 'primary':
                add(dyes, ['Blue', 'White'], c)
                add(dyes, ['Red'], c * 2)
            elif n == 'Orange':
                add(dyes, ['Red', 'Yellow'], c)
            elif n == 'Pink' and type == 'primary':
                add(dyes, ['Red', 'White'], c)

    return dict(sorted(dyes.items(), key=lambda item: item[1], reverse=True))

def add(d: Dict[str, int], keys: List[str], amount: int) -> None:
    for e in keys:
        d[e] = d.get(e, 0) + amount


parser = argparse.ArgumentParser()
parser.add_argument('file', help='path to the csv file containing the material list')
parser.add_argument('--precision', '-p', choices=['shulker', 'stack', 'item'], default='stack', help='lowest precision of the values')
parser.add_argument('--lower', '-l', help='if values are lower than the precision, display them more precisely', action='store_true')
parser.add_argument('--strict', '-S', help='keep all values in the defined precision', action='store_true')
parser.add_argument('--dye', '-d', help='compute the amount of dye needed', choices=['all', 'quasi', 'primary', 'tall', 'prim-no-tall'], default=None)
parser.add_argument('--storage', '-s', help='show how much storage space is needed', action='store_true')

args = parser.parse_args()

if args.lower and args.strict:
    print("--lower and --strict are mutually exclusive. Exiting.")
    sys.exit()

data = dict()
with open(args.file, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data[row['Item']] = int(row['Total'])

if args.dye is not None:
    data = get_dyes(data, args.dye)

longest = len(max(data.keys(), key=len))
for name, count in data.items():
    print_item(name, longest, count)

if args.storage:
    data = {n: math.ceil(c / 64) for n, c in data.items()}
    stacks = sum(data.values())
    print()
    print(f'Total shulker boxes: {math.ceil(stacks / 27)}')
    print(f'Total double chests: {math.ceil(stacks / 54)}')

    args.precision = 'item'
    print_item("Logs & Shulker Shells:", 0, math.ceil(stacks / 27) * 2)
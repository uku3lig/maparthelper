import pandas as pd
import argparse
import math
import sys

from typing import Dict


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

def get_dyes(items: Dict[str, int]) -> Dict[str, int]:
    dyes = {n[:-11]: math.ceil(a / 8) for n, a in items.items() if "Terracotta" in n}
    return dyes


parser = argparse.ArgumentParser()
parser.add_argument('file', help='path to the csv file containing the material list')
parser.add_argument('-p', choices=['shulker', 'stack', 'item'], default='stack', help='lowest precision of the values')
parser.add_argument('-l', help='if values are lower than the precision, display them more precisely', action='store_true')
parser.add_argument('--strict', help='keep all values in the defined precision', action='store_true')
parser.add_argument('--dye', '-d', help='compute the amount of dye needed to', action='store_true')

args = parser.parse_args()

if args.l and args.strict:
    print("-l and --strict are mutually exclusive. Exiting.")
    sys.exit()

data = pd.read_csv(args.file, usecols=['Item', 'Total'], index_col=0).squeeze('columns').to_dict()

if args.dye:
    data = get_dyes(data)
    args.p = 'item'

longest = len(max(data.keys(), key=len))
for name, count in data.items():
    print_item(name, longest, count)
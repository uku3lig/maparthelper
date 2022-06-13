import argparse
import csv
import math
import sys


PRIMARY_DYES = ["Black", "Blue", "Brown", "Green", "Red", "White", "Yellow"]
QUASI_PRIMARY_DYES = ["Light Blue", "Light Gray", "Lime", "Magenta", "Orange", "Pink"]
SECONDARY_DYES = ["Cyan", "Gray", "Purple"]
DYES = PRIMARY_DYES + QUASI_PRIMARY_DYES + SECONDARY_DYES

# concrete is not here since we need to add powder and solid together
# see get_dyes
ONE_FOR_EIGHT = ["Terracotta", "Stained Glass", "Stained Glass Pane"]

TALL_FLOWER_DYES = ["Red", "Pink", "Magenta", "Yellow"]
TALL_FLOWER_CRAFTABLE = ["Orange", "Purple"]

FLOWERS = {
    "Black": "Ink Sac/Wither Rose",
    "Blue": "Lapis Lazuli/Cornflower",
    "Brown": "Cocoa Beans",
    "Green": "Cactus",
    "Red": "Poppy/Red Tulip/Beetroot",
    "White": "Bone Meal/Lily of the Valley",
    "Yellow": "Dandelion",
    "Light Blue": "Blue Orchid",
    "Light Gray": "Azure Bluet/Oxeye Daisy/White Tulip",
    "Lime": "Sea Pickle",
    "Magenta": "Allium",
    "Orange": "Orange Tulip",
    "Pink": "Pink Tulip"
}
TALL_FLOWERS = {
    "Poppy/Red Tulip/Beetroot": "Rose Bush",
    "Dandelion": "Sunflower",
    "Allium": "Lilac",
    "Pink Tulip": "Peony"
}


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

def get_dyes(items: dict, type: str) -> dict:
    # FIXME add conc and conc powder together
    dyes = {dye: 0 for dye in DYES}

    for item, amount in items.items():
        dye = [d for d in DYES if item.startswith(d) and 'Carpet' not in item]
        if len(dye) != 1:
            continue

        if any([item.endswith(e) for e in ONE_FOR_EIGHT]):
            amount = math.ceil(amount / 8)
        elif 'Concrete' in item:
            amount = amount / 8

        dyes[dye[0]] += amount
    
    dyes = {dye: math.ceil(amount) for dye, amount in dyes.items() if amount != 0}

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
            if n in PRIMARY_DYES or (type == 'prim-tall' and n in TALL_FLOWERS):
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
    
    return dyes


def add(d: dict, keys: list, amount: int) -> None:
    for e in keys:
        d[e] = d.get(e, 0) + amount

def replace_keys(d: dict, keys: dict, value_func = None) -> None:
    for k, v in list(d.items()):
        if k in keys.keys():
            d[keys[k]] = d.pop(k) if value_func is None else value_func(d.pop(k))

def convert_file(path: str) -> None:
    with open(path, 'r', newline='') as r:
        reader = csv.reader(r)

        header = next(reader) + ['Done']
        rows = [header]

        for row in reader:
            rows.append(row + ['N'])
        
    with open(path, 'w', newline='') as w:
        writer = csv.writer(w)
        writer.writerows(rows)


def mark_as_done(path: str, key: str) -> None:
    with open(path, 'r', newline='') as r:
        reader = csv.reader(r)

        rows = [next(reader)]
        for row in reader:
            if key in row:
                row[-1] = 'Y'
            rows.append(row)

    with open(path, 'w', newline='') as w:
        writer = csv.writer(w)
        writer.writerows(rows)


def needs_conversion(path: str) -> bool:
    with open(path, 'r', newline='') as r:
        reader = csv.reader(r)
        return 'Done' not in next(reader)


# TODO concrete block amounts (sand and gravel + dyes)
# TODO sandstone?

parser = argparse.ArgumentParser()
parser.add_argument('file', help='path to the csv file containing the material list')
parser.add_argument('--precision', '-p', choices=['shulker', 'stack', 'item'], default='item', help='lowest precision of the values')
parser.add_argument('--lower', '-l', help='if values are lower than the precision, display them more precisely', action='store_true')
parser.add_argument('--strict', '-S', help='keep all values in the defined precision', action='store_true')
parser.add_argument('--dye', '-d', help='compute the amount of dye needed', choices=['all', 'quasi', 'primary', 'prim-tall'], default=None)
parser.add_argument('--flower', '-f', help='when used with -d, shows the amount of items needed to craft the dyes', action='store_true')
parser.add_argument('--storage', '-s', help='show how much storage space is needed', action='store_true')
parser.add_argument('--done', '-D', help='mark a item as done, hiding it from the list', action='store', nargs='+', metavar='name')
parser.add_argument('--show-done', help='show done items with their respective amounts', action='store_true')

args = parser.parse_args()

if args.lower and args.strict:
    print("--lower and --strict are mutually exclusive. Exiting.")
    sys.exit()

if args.done is not None and needs_conversion(args.file):
    convert_file(args.file)


data, done = dict(), dict()
with open(args.file, 'r', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if 'Done' in row and row['Done'] == 'Y':
            done[row['Item']] = int(row['Total'])
        else:
            data[row['Item']] = int(row['Total'])

    if args.done is not None and len(args.done) != 0:
        items = [s.strip() for s in " ".join(args.done).split(",")]
        for item in items:
            t = [k for k in data if item.casefold() == k.casefold()]
            if len(t) != 1:
                print(f'WARNING: could not find {item} in the csv file')
            else:
                t = t[0]
                mark_as_done(args.file, t)
                if t in data:
                    done[t] = data[t]
                    del data[t]
    
        done = dict(sorted(done.items(), key=lambda item: item[1], reverse=True))



if args.dye is not None:
    data = get_dyes(data, args.dye)

    if args.flower:
        replace_keys(data, FLOWERS)
        if 'tall' in args.dye:
            replace_keys(data, TALL_FLOWERS, lambda x: math.ceil(x/2))

    data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))


longest = len(max(data.keys(), key=len))
for name, count in data.items():
    print_item(name, longest, count)

if args.show_done:
    print('\nDone:')
    for name, count in done.items():
        print_item(name, longest, count)

if args.storage:
    data = {n: math.ceil(c / 64) for n, c in data.items()}
    stacks = sum(data.values())
    print()
    print(f'Total shulker boxes: {math.ceil(stacks / 27)}')
    print(f'Total double chests: {math.ceil(stacks / 54)}')

    args.precision = 'item'
    print_item("Logs & Shulker Shells:", 0, math.ceil(stacks / 27) * 2)
# maparthelper 
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/uku3lig/maparthelper?include_prereleases&style=for-the-badge)](https://github.com/uku3lig/maparthelper/releases/latest)
[![wakatime](https://wakatime.com/badge/github/uku3lig/maparthelper.svg?style=for-the-badge)](https://wakatime.com/badge/github/uku3lig/maparthelper)

**maparthelper** is a simple python tool that helps you with maparts (and schematics in general) to compute the amount of materials needed and many more things!

### How to use 

Grab the [latest release](https://github.com/uku3lig/maparthelper/releases/latest) and download the file corresponding to your platform. For now the program needs to be ran from a terminal to work.

#### Available options

Parameter | Short | Choices | Explanation
---|---|---|---
`--precision` | `-p` | `shulker`, `stack`, `item` | Sets the minimum unit to display the materials.
`--lower` | `-l` | None | If some material has less than the minimum unit, display the amount more precisely.
`--strict` | `-S` | None | Keep all the values in the defined precision with `-p`, no lower, no higher.
`--dye` | `-d` | `all`, `quasi`, `primary`, `prim-tall` | Calculates the amount of dye needed to dye terracotta. See [this section](#dye-options).
`--flower` | `-f` | None | When used with `-d`, shows the materials needed to craft all the dyes.
`--storage` | `-s` | None | Show the amount of storage space needed to store all the materials.
`--done` | `-D` | comma-separated list of items | Marks the specified items as done, hiding them from the material list.
`--show-done` | None | None | Shows the items marked as done.

#### `--dye` options

Option | Explanation
---|---
`all` | Show all types of dye.
`quasi` | Show only primary and [quasi-primary dyes](https://minecraft.fandom.com/wiki/Dye#Quasi-Primary).
`primary` | Show only primary dyes.
`prim-tall` | Show only primary dyes and dyes that can be created from tall flowers (pink & magenta).

### Building/Running from source

Running: `python3 maparthelper.py [args]`

Building: Install the `pyinstaller` module (with pip: `pip install pyinstaller`) and run `pyinstaller -F --noconsole maparthelper.py`. The resulting binary will be output in the `dist` folder;

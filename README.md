# Linux Scripts for Workstation

## Overview

This script installs a few things on the workstation

* A `.bashrc` file (starts tmux, sets PS1, sets PATH, and does a few other things)
* A `.tmux.conf` file
* A `.vimrc` file and a `.vim` directory for plugins, etc.
* A `~/bin/` directory which contains standard scripts I want on all my
  workstations.
* A `~/.bash_aliases` file which gets loaded by ~/.bashrc with helpful pre-set
  commands.

The effect of this is that all linux workstations that I will spend any amount
of time on (> 1 hour) can now have my shell environment installed on it that
I am familiar with.

## Getting Started

```bash
cd ~
git clone https://github.com/frankbryce/linux_scripts.git
./linux_scripts/bin/mypull
# restart bash
```

## To Pull

```bash
# this is added to your PATH automatically on startup
mypull
```

## To Push a File Back to the Repo

```bash
# this is added to your PATH automatically on startup
cd ~
mypush <rel_path_to_file>
```

## To Delete a File in the Repo

TODO: add this to the push functionality

```bash
cd ~
FILE_TO_DELETE=<rel_path_to_file>
cd linux_scripts
git rm -r $FILE_TO_DELETE
git commit
cd ~
rm -r $FILE_TO_DELETE
```


# Linux Scripts for Workstation

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

# To Push a File Back to the Repo

```bash
# this is added to your PATH automatically on startup
cd ~
mypush <rel_path_to_file>
```

# To Delete a File in the Repo

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


# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
	. "$HOME/.bashrc"
    fi
fi

# values for google source code locations
export head=/google/src/head/depot/google3
export citc_root=/google/src/cloud/jcarp/
export ebin=experimental/users/jcarp/bin
export gbin=$head/$ebin

# personal env vars
# export PAYMENTS_CELLS="im it jx yi yv"
export PAYMENTS_CELLS="im jx yi yv"
export MY_CELLS=$PAYMENTS_CELLS

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$PATH:$HOME/bin:$gbin"
fi

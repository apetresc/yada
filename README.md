# YADA

[![Build Status](https://travis-ci.com/apetresc/yada.svg?branch=master)](https://travis-ci.com/apetresc/yada)
[![PyPI version](https://badge.fury.io/py/yada.svg)](https://badge.fury.io/py/yada)

Yet Another Dotfile Aggregator


## Install

Yada is distributed via PyPI, so installation is simply a matter of

    $ pip install yada

On Arch Linux, it is also available on the [AUR](https://aur.archlinux.org/packages/yada).


## Configure

Yada's own configuration is located in `~/.config/yada/config.yaml`, and is automatically created
on the first command. The only value that _needs_ to change is `username`, if your Github username
differs from your OS account name.


## Concepts

The two important entities in Yada are:

  - A **module** is a related set of configuration files and hooks, usually (but not always) in a
    one-to-one correspondence with a single program.
    - For example, you might have a `vim` module and an `i3` module.
  - A **repository** is a collection of modules that are distributed together, and almost always
    is backed by a Git repository. Most people only ever need one of these ever, although you may
    want several if:
    - you want separate

## Usage

You can see a list of all of Yada's commands with:

```
    $ yada
    Usage: yada [OPTIONS] COMMAND [ARGS]...

    Options:
      --dry-run / --no-dry-run  don't actually make any changes to the filesystem
      --yada-home DIRECTORY     directory to store yada modules in
      --help                    Show this message and exit.

    Commands:
      home     print path to the repo
      import   import an existing file into a module
      info     print a helpful summary of a module's contents and changes
      init     create a brand new dotfile repo
      install  symlink all files from a module into $HOME
      pull     pull new changes to the repo
      push     scp a module to a remote SSH host
      version  print version number and exit
```

The most important commands are described below in more detail, roughly in the order in which you
will first encounter them.

### `init`

Creates a brand new empty repository. 

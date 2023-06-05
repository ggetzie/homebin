# Migration plan for kotsf.com

## Install dependencies on new server

postgresql-14, postgresql-14-postgis-3, nginx, redis, [python dependencies](https://devguide.python.org/getting-started/setup-building/index.html#install-dependencies)
with dependencies for all optional modules.

## Set up git and ssh

- Make sure git is installed.
- create ssh key and add to git
- install ssh public key on old server

## Install homebin and add to $PATH

```
git clone git@github.com:ggetzie/homebin.git bin
```

## Move over sites from old server

### ASLCV2

### askreddit_but_ai

### vyfntp

### mscv2

### J2020_0003

### kotsf_biz

### tiltingatwindmills

### books

- Set up calibre on new server
- rsync library from older server
- copy over user db

### greaterdebater (tcd)

Copy nginx conf file over

## Redirect DNS to new server

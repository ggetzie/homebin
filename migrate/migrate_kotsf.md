# Migration plan for kotsf.com

## Install dependencies on new server

supervisor, postgresql-14, postgresql-14-postgis-3, nginx, redis, [python dependencies](https://devguide.python.org/getting-started/setup-building/index.html#install-dependencies)
with dependencies for all optional modules.

## Set up git and ssh

- Make sure git is installed.
- create ssh key and add to git
- install ssh public key on old server

## Clone homebin and add to $PATH

```
git clone git@github.com:ggetzie/homebin.git bin

# add to .bash_profile
PATH=/home/ubuntu/bin:${PATH}
export PATH
```

## create webapps group and add ubuntu user to it

## Move over sites from old server

### ASLCV2
- Create app user
- clone the repository
- Create virtual environment and install dependencies
- copy over env file
- set up database
- copy over media files
- link supervisor and nginx conf files

### askreddit_but_ai

### vyfntp
- create app user
- clone repository
- create virtual environment
- copy over .env file
- set up database
- copy media files
- link supervisor and nginx conf files
- create logs
  
### mscv2

### J2020_0003

### kotsf_biz
- done
### tiltingatwindmills

### books

- Set up calibre on new server
- rsync library from older server
- copy over user db
- copy nginx conf file

### greaterdebater (tcd)

Copy nginx conf file over

## Redirect DNS to new server

## Set up classroom gallery

### create app user
### clone repository
### setup dotenv file
### create environment and install requirements.txt
### setup database
### link srv files
### install ssl certificate

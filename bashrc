# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
export HISTCONTROL=ignoredups

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
# case "$TERM" in
# xterm-color)
#     PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
#     ;;
# *)
#     PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
#     ;;
# esac

alias xterm='xterm -font -*-fixed-medium-r-*-*-18-*-*-*-*-*-iso8859-*'

# load xterm defaults
xrdb -load ~/.Xdefaults

# Comment in the above and uncomment this below for a color prompt
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\W\[\033[00m\]\$ '

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME}: ${PWD/$HOME/~}\007"'
    ;;
*)
    ;;
esac

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable color support of ls and also add handy aliases
if [ "$TERM" != "dumb" ]; then
    eval "`dircolors -b`"
    alias ls='ls --color=auto'
    #alias dir='ls --color=auto --format=vertical'
    #alias vdir='ls --color=auto --format=long'
fi

# swap left control and caps lock
# xmodmap ~/.Xmodmap

# some more ls aliases
#alias ll='ls -l'
#alias la='ls -A'
#alias l='ls -CF'
alias mscheme='scheme -large -edit'

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi

export PYTHONPATH=${PYTHONPATH}:'/home/gabe/python':''
PATH="$PATH:/home/gabe/android/android-sdk-linux/tools"
JAVA_HOME="$JAVA_HOME:/usr/lib/jvm/java-7-openjdk-amd64/bin/"

alias ssh9="ssh -p 19999"
alias backup="rsync -vaxEe 'ssh -p 19999' --delete --exclude='.cache' ~ '/media/gabe/My Book/backup/'"

alias phonesync="rsync -vaxEe --delete /media/GalaxyNexus/ /media/data/phone/gnex"
alias PMS="sudo /home/gabe/downloads/pms-1.90.1/PMS.sh"
alias gdenv="source /home/gabe/python/env/gd/bin/activate"
alias cva="source /home/gabe/python/env/ceavy/bin/activate"
alias cvea="source /home/gabe/python/env/cveng/bin/activate"
alias cash="source /usr/local/src/env/cash/bin/activate"
alias recash="sudo supervisorctl restart cashcal"
alias sbenv="source /usr/local/src/env/sblog/bin/activate"
alias haus="source ~/Dropbox/code/houses/env/haus/bin/activate"
alias fans="sudo pstate-frequency --set --plan performance"

alias proph="cd /usr/local/src/prophit_dev/prophit_main_repo"
alias penv="source '/usr/local/src/env/prophit/local/bin/activate'"
alias repro="sudo supervisorctl restart prophit_main celery"

alias aeq="cd /usr/local/src/aeq"
alias reaeq="sudo supervisorctl restart aeq"
alias aeqenv="source /usr/local/src/env/aeqenv/bin/activate"


alias dsenv="source ~/python/env/ds/bin/activate"
alias ds3env="source ~/python/env/ds3/bin/activate"

alias pcp="cd /usr/local/src/pcp/"
alias repcp="sudo supervisorctl restart pcp"
alias pcpenv="source /usr/local/src/env/postcard-prank/bin/activate"


# N-Triples aliases from http://blog.datagraph.org/2010/03/grepping-ntriples
alias rdf-count="awk '/^\s*[^#]/ { n += 1 } END { print n }'"
alias rdf-lengths="awk '/^\s*[^#]/ { print length }'"
alias rdf-length-avg="awk '/^\s*[^#]/ { n += 1; s += length } END { print s/n }'"
alias rdf-length-max="awk 'BEGIN { n=0 } /^\s*[^#]/ { if (length>n) n=length } END { print n }'"
alias rdf-length-min="awk 'BEGIN { n=1e9 } /^\s*[^#]/ { if (length>0 && length<n) n=length } END { print (n<1e9 ? n : 0) }'"
alias rdf-subjects="awk '/^\s*[^#]/ { print \$1 }' | uniq"
alias rdf-predicates="awk '/^\s*[^#]/ { print \$2 }' | uniq"
alias rdf-objects="awk '/^\s*[^#]/ { ORS=\"\"; for (i=3;i<=NF-1;i++) print \$i \" \"; print \"\n\" }' | uniq"
alias rdf-datatypes="awk -F'\x5E' '/\"\^\^</ { print substr(\$3, 2, length(\$3)-4) }' | uniq"

# disable touchpad
# xinput --set-prop "SynPS/2 Synaptics TouchPad" "Device Enabled" 1

export PATH="/usr/local/src/aeq/bin:/home/gabe/bin:$PATH"

# added by Anaconda3 2.3.0 installer
export PATH="/home/gabe/python/anaconda3/bin:$PATH"

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
PYTHON_BUILD_MIRROR_URL="http://yyuu.github.io/pythons"

alias lr="cd /usr/local/src/learn-react"
alias cvenv="source /usr/local/src/env/ceevee/bin/activate"
alias recv="sudo supervisorctl restart ceevee"
alias mscv="cd /usr/local/src/ceevee"
alias cf="cd /usr/local/src/learn-react/cashflo_0-1"
alias mdulenv="source /usr/local/src/env/mdul/bin/activate"

export PATH="$HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH"
alias nnrenv="source /usr/local/src/env/nnr/bin/activate"
alias nnr="cd /usr/local/src/nnr"
alias nnr="cd /usr/local/src/nnr"
alias rennr="sudo supervisorctl restart nnr"

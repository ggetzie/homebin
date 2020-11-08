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
export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64/bin/"

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

export PATH="/home/gabe/bin:/usr/lib/postgresql/12/bin:/home/gabe/android/android-sdk-linux/tools:/home/gabe/.local/bin:$PATH"
export PATH="$HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH"
# added by Anaconda3 2.3.0 installer
# export PATH="/home/gabe/python/anaconda3/bin:$PATH"

# export PYENV_ROOT="$HOME/.pyenv"
# export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init -)"
# PYTHON_BUILD_MIRROR_URL="http://yyuu.github.io/pythons"

export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools

alias lr="cd /usr/local/src/learn-react"
alias cvenv="source /usr/local/src/env/ceevee/bin/activate"
alias recv="sudo supervisorctl restart ceevee"
alias mscv="cd /usr/local/src/ceevee"
alias cf="cd /usr/local/src/learn-react/cashflo_0-1"
alias mdulenv="source /usr/local/src/env/mdul/bin/activate"

alias screen-nnr="screen -S nnr -c /home/gabe/bin/.screenrc-nnr"
alias screen-bfm="screen -S bfm -c /home/gabe/bin/.screenrc-bfm"
alias screen-aeq="screen -S aeq -c /home/gabe/bin/.screenrc-aeq"
alias screen-fvdw="screen -S fvdw -c /home/gabe/bin/screen/.screenrc-fvdw"
alias screen-blog="screen -S blog -c /home/gabe/bin/screen/.screenrc-blog"
alias screen-base="screen -S work -c /home/gabe/bin/screen/.screenrc-base"

alias nnrenv="source /usr/local/src/env/nnr/bin/activate"
alias nnr="cd /usr/local/src/nnr"
alias rennr="sudo supervisorctl restart nnr"
alias homenv="source /usr/local/src/env/home/bin/activate"
alias nnrfwd="stripe listen --forward-to nnr/main/webhook/"
alias recv="sudo supervisorctl restart ceevee"
alias bfmenv="source /usr/local/src/env/J2020_0001/bin/activate"
alias bfm="cd /usr/local/src/J2020_0001"
alias py38="source /usr/local/src/env/py38/bin/activate"
alias aeqcmsenv="source /usr/local/src/env/aeqcms/bin/activate"
alias aeqcms="cd /usr/local/src/aeqcms"
alias mscv2env="source /usr/local/src/env/mscv2/bin/activate"
alias mscv2="cd /usr/local/src/mscv2"
alias aeq="cd /usr/local/src/aeq"
alias aeq2="cd /usr/local/src/aeq2"
alias aeqenv="source /usr/local/src/env/aeq/bin/activate"
alias reaeq="sudo supervisorctl restart aeq"
alias J2020_0003env="source /usr/local/src/env/J2020_0003/bin/activate"
alias cvengenv="source /usr/local/src/env/cveng/bin/activate"
alias araienv="source /usr/local/src/env/arai/bin/activate"
alias fvdw_backendenv="source /usr/local/src/env/fvdw_backend/bin/activate"
alias kotsf_bizenv="source /usr/local/src/env/kotsf_biz/bin/activate"
alias aslcv2_beenv="source /usr/local/src/env/aslcv2_be/bin/activate"
alias caktus_tddenv="source /usr/local/src/env/caktus_tdd/bin/activate"
alias exp_tastenv='source /usr/local/src/env/exp_taste/bin/activate'
alias aslcv2="cd /home/gabe/Dropbox/kotsf/Projects/J2020_0007_PeterCobb/code/aslcv2"
alias exp_tasteenv="source /usr/local/src/env/exp_taste/bin/activate"
alias timekeeperenv="source /usr/local/src/env/timekeeper/bin/activate"
alias eg_psatenv="source /usr/local/src/env/eg_psat/bin/activate"
alias hkuvpn='/opt/cisco/anyconnect/bin/vpn connect vpn2fa.hku.hk'
alias hkuvpnd="/opt/cisco/anyconnect/bin/vpn disconnect vpn2fa.hku.hk"

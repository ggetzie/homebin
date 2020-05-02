# homebin
short helpful scripts for /home/$USER/bin

- `keygen`: Create a string of random characters of desired length (for passwords, secret keys, etc).

- `lm`: `less` the most recently added file for a given directory

- `link-srv`: for my standard Django project setup. Create symbolic links from repository for nginx, supervisor config files

- `lsp`: pipe output from `ls` through `less`, preserving colors, so you can page through large directories

- `make-logs`: create logs directory and touch commonly used log files for Django projects

- `passphrase`: create a passphrase of randomly selected words from the given dictionary file. Tries to use /usr/share/dict/american-english by default. Optionally, randomly replace characters with "133+" speak equivalents.

- `setup-keys`: generate passwords and secret keys for standard Django project

- `sshnopass`: start the ssh-agent and add key so you don't have to keep retyping the password.

- `startscreen`: create the directory GNU Screen needs to run if it doesn't exist.

- `surface-restart.sh`: startup nginx, postgress, and supervisor after restarting WSL

- `whowin`: randomly select a winner from two options with weighting by seed ranking. Used for filling out March Madness brackets

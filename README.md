# homebin
short helpful scripts for /home/$USER/bin

- `countries.txt`: List of all countries in the world

- `convert_dotenv`: Copy environment variables from venv activate file to separate .env file in project directory

- `db_perms`: Quickly grant a user permissions to all objects in Postgres database.

- `get_vars`: Look for environment variables used in Django settings files

- `keygen`: Create a string of random characters of desired length (for passwords, secret keys, etc).

- `lm`: `less` the most recently added file for a given directory

- `link_srv`: for my standard Django project setup. Create symbolic links from repository for nginx, supervisor config files

- `lsp`: pipe output from `ls` through `less`, preserving colors, so you can page through large directories

- `make_logs`: create logs directory and touch commonly used log files for Django projects

- `passphrase`: create a passphrase of randomly selected words from the given dictionary file. Tries to use /usr/share/dict/american-english by default. Optionally, randomly replace characters with "133+" speak equivalents.

- `productivity`: Add/Remove a list of sites to block in your /etc/hosts file

- `sc`: shortcut to start GNU screen with a specified .screenrc file. See the screen directory.

- `setup_db`: Add a new user and database owned by that user to Postgres

- `setup_dotenv`: Create a .env file for your Django project with some default values

- `export_dotenv`: Add all the environment variables in your .env file to your local environment

- `unset_dotenv`: Remove all the environment variables in your .env file from your local environment

- `setup_user`: Create a new OS system user and optionally the webapps group if it doesn't exist

- `sshnopass`: start the ssh-agent and add key so you don't have to keep retyping the password.

- `startscreen`: create the directory GNU Screen needs to run if it doesn't exist.

- `surface-restart.sh`: startup nginx, postgres, and supervisor after restarting WSL

- `table_owner`: Assign all tables in a Postgres database to a new owner

- `update_go`: download and install the specified Golang version

- `whowin`: randomly select a winner from two options with weighting by seed ranking. Used for filling out March Madness brackets

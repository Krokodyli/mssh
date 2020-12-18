# MSSH - My SSH
Simple alias manager for ssh and scp command, that remembers your servers' usernames, ports, identity keys path and server domains. I've written this script to connect to my ssh servers faster and without the need to look for those informations.
## Usage
```
MSSH - simple alias manager for ssh and scp command.
Usage:
mssh l <NAME> - logs into saved SSH server with name <NAME>
mssh d <NAME> <FILE> - downloads file with path <FILE> to current directory from saved SSH server with name <NAME>
mssh u <NAME> <FILE> - uploads file with path <FILE> to home directory in saved SSH server with name <NAME>

mssh s - shows saved SSH servers
mssh a <NAME> <USER> <ADDRESS> <PORT> <IDENTITY FILE OPTIONAL> - saves new SSH server in script config
mssh r <NAME> - removes saved SSH server from script config
```

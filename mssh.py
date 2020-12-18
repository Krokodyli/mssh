#!/usr/bin/env python3

import os
import sys
import json

def getCmdArguments(config, name):
    if name not in config:
        print(name, 'not found in config file.')
        exit(1)

    if 'address' in config[name]:
        address = config[name]['address']
    else:
        print('Invalid config. Address not found.')
        exit(1)

    if 'user' in config[name]:
        user = config[name]['user']
    else:
        print('Invalid config. Username not found.')
        exit(1)

    if 'port' in config[name]:
        port = config[name]['port']
    else:
        port = 22

    if 'key' in config[name]:
        key = config[name]['key']
    else:
        key = ''

    return user, address, port, key

def loadConfig(path):
    try:
        file = open(path, 'r')
        config = json.load(file)
    except Exception as e:
        print('Exception:', e)
        exit(1)
    finally:
        if 'file' in locals() and not file.closed:
            file.close()
    return config

def saveConfig(path, config):
    try:
        file = open(path, 'w')
        json.dump(config, file)
    except Exception as e:
        print('Exception:', e)
        exit(1)
    finally:
        if not file.closed:
            file.close()

def main(argv):
    # Load config
    configLocation = os.path.dirname(os.path.realpath(__file__)) + '/config.json'

    config = loadConfig(configLocation)

    wrongArgsFlag = False
    if len(argv) == 1:
        if argv[0] == '-h' or argv[0] == 'h':
            print('MSSH - simple alias manager for ssh and scp command.')
            print('Usage:')
            print('mssh l <NAME> - logs into saved SSH server with name <NAME>')
            print('mssh d <NAME> <FILE> - downloads file with path <FILE> to current directory from saved SSH server with name <NAME>')
            print('mssh u <NAME> <FILE> - uploads file with path <FILE> to home directory in saved SSH server with name <NAME>')
            print()
            print('mssh s - shows saved SSH servers')
            print('mssh a <NAME> <USER> <ADDRESS> <PORT> <IDENTITY FILE OPTIONAL> - saves new SSH server in script config')
            print('mssh r <NAME> - removes saved SSH server from script config')
        elif argv[0] == 's':
            if len(config) > 0:
                print('Saved SSH servers:')
                for server in config.items():
                    print('    ', server[0], ':', sep='')
                    if 'address' in server[1]:
                        print('        address: ', server[1]['address'], sep='')
                    if 'user' in server[1]:
                        print('        user: ', server[1]['user'], sep='')
                    if 'port' in server[1]:
                        print('        port: ', server[1]['port'], sep='')
                    if 'key' in server[1]:
                        print('        identity file path: ', server[1]['key'], sep='')
            else:
                print('There are no saved servers')
        else:
            wrongArgsFlag = True
    elif len(argv) == 2:
        name = argv[1]
        # Log into your ssh server
        if argv[0] == 'l':
            user, address, port, key = getCmdArguments(config, name)
            if key == '':
                exit(os.system('ssh -p '+port+' '+user+'@'+address))
            else:
                exit(os.system('ssh -i '+key+' -p '+port+' '+user+'@'+address))
        # Delete ssh server from config
        elif argv[0] == 'r':
            if argv[1] in config:
                config.pop(argv[1])
                print('Removed \''+argv[1]+'\'.')
                saveConfig(configLocation, config)
            else:
                print('There is no saved ssh server with this name.')
        else:
            wrongArgsFlag = True
    elif len(argv) == 3:
        name = argv[1]
        filename = argv[2]
        # Upload file
        if argv[0] == 'u':
            user, address, port, key = getCmdArguments(config, name)
            if key == '':
                exit(os.system('scp -P '+port+' '+filename+' '+user+'@'+address+':'))
            else:
                exit(os.system('scp -i '+key+' -P '+port+' '+filename+' '+user+'@'+address+':'))
        # Download file
        elif argv[0] == 'd':
            user, address, port, key = getCmdArguments(config, name)
            if key == '':
                exit(os.system('scp -P '+port+' '+user+'@'+address+':'+filename+' '+'.'))
            else:
                exit(os.system('scp -i '+key+' -P '+port+' '+user+'@'+address+':'+filename+' '+'.'))
        else:
            wrongArgsFlag = True
    elif len(argv) == 5 or len(argv) == 6:
        if argv[0] == 'a':
            name = argv[1]
            newServer = {}
            newServer['user'] = argv[2]
            newServer['address'] = argv[3]
            newServer['port'] = argv[4]
            if len(argv) == 6:
                newServer['key'] = argv[5]
            config[name] = newServer
            saveConfig(configLocation, config)
        else:
            wrongArgsFlag = True
    else:
        wrongArgsFlag = True

    if wrongArgsFlag:
        print('Invalid arguments. Type \'mssh h\' for summary of options.')


if __name__ == '__main__':
    main(sys.argv[1:])

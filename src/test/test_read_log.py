import os
try:
    commands = []
    with open('log.txt', 'r+') as logfile:
        for line in logfile.readlines():
            commands.append(line.strip('\n'))
    os.remove('log.txt')

except:
    pass



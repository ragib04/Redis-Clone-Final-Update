def log(funcn, *args):
    command = [funcn]
    for i in args:
        command.append(i)
    command = ' '.join(command)
    command = command.strip(' ')
    command += '\n'
    print(command)
    with open("log.txt", "a") as log_file:
        log_file.write(command)

query = "myzset 2 two 3 three 4 four 5 five CH"
log('SET', *query.split(' '))

from flask import Flask
from src.functions import Redis
from src.exception import *
import os
import time
import traceback

redis_obj = Redis()


def load_log():
    print('in load_log()')
    commands = []
    try:
        with open('log.txt', 'r+') as logfile:
            for line in list(logfile):
                cmd = line.strip().split()
                commands.append((float(cmd[0]), ' '.join(cmd[1:])))
        os.remove('log.txt')
    except:
        pass
    try:
        for cmd in commands:
            redis_process(*cmd)
        keys = list(redis_obj.hash_table.keys())
        for key in keys:
            redis_obj.destroy_util(time.time(), key)
        print('log loaded successfully.')
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        print("ERR. Couldn't load previous data.")


def redis_process(curr_time, command):
    print(f'in redis_process() with "{command}"')
    command = command.split()
    response = None
    if command[0].lower() == 'get':
        try:
            response = redis_obj.GET(curr_time, *command[1:])
        except NoStringValueError:
            response = "Returned value is not String"
    elif command[0].lower() == 'set':
        try:
            response = redis_obj.SET(curr_time, *command[1:])
        except InvalidRequest:
            response = "Request Invalid"
    elif command[0].lower() == 'expire':
        response = redis_obj.EXPIRE(curr_time, *command[1:])
    elif command[0].lower() == 'zadd':
        try:
            response = redis_obj.ZADD(curr_time, *command[1:])
        except SyntaxError:
            response = "Syntax Error in Command"
        except InvalidDataType:
            response = "Wrong Data Type"
    elif command[0].lower() == 'zrank':
        try:
            response = redis_obj.ZRANK(curr_time, *command[1:])
        except InvalidDataType:
            response = "Only sets can be queried for Zrank"
    elif command[0].lower() == 'zrevrank':
        try:
            response = redis_obj.ZREVRANK(curr_time, *command[1:])
        except InvalidDataType:
            response = "Only sets can be queried for ZRevRank"
    elif command[0].lower() == 'zrange':
        try:
            response = redis_obj.ZRANGE(curr_time, *command[1:])
        except SyntaxError:
            response = "Syntax Error in Command"
        except InvalidFormat:
            response = "Invalid format"
        except InvalidDataType:
            response = "Only sets can be queries for ZRange"
    elif command[0].lower() == 'zrevange':
        try:
            response = redis_obj.ZREVRANGE(curr_time, *command[1:])
        except SyntaxError:
            response = "Syntax Error in Command"
        except InvalidFormat:
            response = "Invalid format"
        except InvalidDataType:
            response = "Only sets can be queries for ZREVRange"
    elif command[0].lower() == 'del':
        response = redis_obj.DELETE(curr_time, *command[1:])
    elif command[0].lower() == 'ttl':
        response = redis_obj.TTL(curr_time, *command[1:])
    elif command[0].lower() == 'ping':
        response = redis_obj.ping()
    else:
        response = f'ERR Unknown or disabled command "{command[0]}"'
    return response


class RedisFlaskServer(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        with self.app_context():
            load_log()
        super(RedisFlaskServer, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app = RedisFlaskServer(__name__)


@app.route('/')
def hello():
    return 'Hello!!! Welcome to REDIS_CLONE!!!'


@app.route('/<command>', methods=['GET'])
def redis(command):
    print(f'in redis() with "{command}"')
    return redis_process(time.time(), command)


@app.route('/curr_status', methods=['GET'])
def current():
    return str(redis_obj)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True, use_reloader=False)


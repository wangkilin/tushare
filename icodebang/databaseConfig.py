#coding=utf8
config = {
    'host':'127.0.0.1',
    'user':'root', 
    'password':'4728999', 
    'database':'WeCenter', 
    'charset':'utf8'
}

config['connect'] = 'mysql://'+config['user']
if (config['password']) :
    config['connect'] += ':' + config['password']
config['connect'] += '@' + config['host'] + '/' + config['database']
if (config['charset']) :
    config['connect'] += '?charset=' + config['charset']
    
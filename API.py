import bottle
from bottle import request, response
from bottle import post, get, put, delete
import re, json
from db_connector import unblock, block, add_to_cannot_block

ip_pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


def _validate_ip(data):
    if data is None:
        raise ValueError
    try:
        if ip_pattern.match(data['ip']) is None:
            raise ValueError
        return data['ip']
    except:
        raise ValueError

@post('/block')
def block_handler():
    '''Handles a block request'''
    try:
        data = _validate_ip(request.POST)
    except ValueError:
        response.status = 400
        return json.dumps({'Error': ValueError})
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    status = block(client_ip, data)
    #response.headers['Content-Type'] = 'application/json'
    return json.dumps({'Status': status})

@post('/unblock')
def unblock_handler():
    '''Handles a block request'''
    try:
        data = _validate_ip(request.POST)
    except ValueError:
        response.status = 400
        return json.dumps({'Error': ValueError})
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    status = un_block(client_ip, data)
    #response.headers['Content-Type'] = 'application/json'
    return json.dumps({'Status': status})


#find better name
@post('/add')
def add_handler():
    '''Handles a add request'''
    try:
        data = _validate_ip(request.POST)
    except ValueError:
        response.status = 400
        return json.dumps({'Error': ValueError})
    status = add_to_cannot_block(data)
    #response.headers['Content-Type'] = 'application/json'
    return json.dumps({'Status': status})

bottle.run(host = '127.0.0.1', port = 5000)

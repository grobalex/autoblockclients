import pymysql.cursors
from pymysql.err import IntegrityError
from os import path
import requests
import re
import configparser

######## Callable Methods #########
#    Should be called from API    #
###################################

def block(client_ip, ip_to_block):
    '''
    Tries to _connect to the database and if successful tries to write
    to table. If unsuccessful will log error in the errors table and
    send a slack message
    '''
    if _can_block(ip_to_block):
        sql = "INSERT INTO `blocked_ips` (`client_ip`, `blocked_ip`) VALUES (%s, %s)"
        return _write(sql, (client_ip, ip_to_block), "block")
    else:
        _catch_errors((client_ip, ip_to_block, "block", "Client tried to add ip to the block table but it is on the cannot block list"))
        return "Error - Cannot block this IP"

def add_to_cannot_block(cannot_block_ip):
    '''
    Tries to _connect to the database and if successful tries to write
    to table. If unsuccessful will log error in the errors table and
    send a slack message
    '''
    return _write("INSERT INTO `cannot_block` (`ip`) VALUES (%s)", (cannot_block_ip,), "add")

######## Protected Methods ########
# Should never be called from API #
###################################

## GENERIC DB METHODS ##

def _connect():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return pymysql.connect(host=config.get("configuration","dbhost"),
                                 port=int(config.get("configuration","dbport")),
                                 user=config.get("configuration","dbuser"),
                                 password= config.get("configuration","dbpassword"),
                                 db=config.get("configuration","dbschema"),
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

def _create_db(filename):
    '''
    Creates the required DB when running the program for the first time
    '''
    if path.isfile(filename) is False:
        print("File load error : {}".format(filename))
        return False
    else:
        with open(filename, "r") as sql_file:
            ret = sql_file.read().split(';')
            print(ret)


def _write(sql, vars, action=None):
    '''
    Write to DB
    '''
    connection = _connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, vars)
        connection.commit()
        connection.close()
        return "Success"
    except IntegrityError as e:
        error = re.sub(r'([^\s\w.-]|_)+', '', str(e))
        _catch_errors(vars + (action, error))
        return error

def _read(sql, vars):
    '''
    Read from DB
    '''
    connection = _connect()
    with connection.cursor() as cursor:
        cursor.execute(sql, vars)
        result = cursor.fetchone()
    connection.close()
    return result

def _catch_errors(vars):
    '''
    Catch errors and write to the error DB
    '''
    sql = "INSERT INTO `errors`"
    if len(vars) == 3:
        sql = sql + "(`client_ip`, `action`, `msg`) VALUES (%s, %s, %s)"
    else:
        sql = sql + "(`client_ip`, `blocked_ip`, `action`, `msg`) VALUES (%s, %s, %s, %s)"
    _write(sql, vars)
    _send_to_slack(vars[-1])

def _send_to_slack(msg):
    '''
    Sends a slack message
    '''
    config = configparser.ConfigParser()
    config.read("config.ini")
    requests.post(config.get("configuration","slack"), json={'text': msg})

## IP BLOCK DB METHODS ##

def _can_block(ip_to_block):
    '''
    Checks the ip against the cannot be block DB table and throws an
    error if we try to block that IP.
    '''
    return _read("SELECT `ip` FROM `cannot_block` WHERE `ip`=%s", (ip_to_block,)) is None

_create_db("Dump20190604.sql")

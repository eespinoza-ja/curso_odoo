#!/usr/bin/python3.6
import json
import random
import urllib.request

HOST = 'localhost'
PORT = 8069
DB = 'odoo_db'
USER = 'admin'
PASS = 'admin'

def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type":"application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]

def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})

# Log in the Given Database
url = "http://%s:%s/jsonrpc" % (HOST, PORT)
uid = call(url, "common", "login", DB, USER, PASS)
print("UID: "+str(uid))

# Create a new Session
args = {
    'name': 'Nueva Sesión',
    'course_id': 1,
}
session_id = call(url, "object", "execute", DB, uid, PASS, 'openacademy.session', 'create', args)

# Search Sessions
args = {
    'name',
    'seats'
}
sessions = call(url, "object", "execute", DB, uid, PASS, 'openacademy.session', 'search_read', [],['name','seats'])
for session in sessions:
    print("Session %s (%s seats)" % (session['name'], session['seats']))
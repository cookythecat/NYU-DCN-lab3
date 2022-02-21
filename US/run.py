from ast import Param
from flask import Flask, request
import socket
import iptools
import requests

app = Flask(__name__)
necessary = ['hostname', 'fs_port', 'number', 'as_ip', 'as_port']

def dic_construction(s):
    s_ls = s.split('\n')
    dic = {}
    for e in s_ls:
        e_splited = e.split('=')
        if len(e_splited) != 2:
            continue
        dic[e_splited[0]] = e_splited[1]
    return dic

@app.route("/fibonacci", methods = ['GET'])
def fibonacci():
    args = request.args
    for field in necessary:
        if field not in necessary:
            return "Bad Request, missing arguments", 400
    if not args['as_port'].isdigit() or not args['fs_port'].isdigit():
        return "port must be a postive integr", 400
    if not args['number'].isdigit():
        return "provided number X is not a positive integer", 400
    if not iptools.ipv4.validate_ip(args['as_ip']):
        return "provided ip is not valid", 400
    print(args)
    
    # request fibonacci ip
    fs_ip = None
    fs_port = args['fs_port']
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3000)
    msg = "TYPE=A\nNAME={}".format(args['hostname'])
    try:
        sock.sendto(msg.encode(), (args['as_ip'], int(args['as_port'])))
        reply, addrr = sock.recvfrom(2048)
        reply = reply.decode()
        sock.close()
    except:
        return "UDP request failed", 400
    finally:
        sock.close()

    if reply != "Bad Request":
        dic = dic_construction(reply)
        fs_ip = dic['VALUE']
    else:
        return "Bad request, DNS request failed", 400

    # fibonacci request
    params = {
        'number': int(args['number'])
    }
    return requests.get('http://' + fs_ip + ':' + fs_port + '/fibonacci', params=params).content
    
app.run(host='0.0.0.0',port=8080, debug=True)
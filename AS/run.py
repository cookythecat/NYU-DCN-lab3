import socket
import json

PORT = 53533

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT))
fname = "storage.json"
registration_fields = ['TYPE', 'NAME', 'VALUE', 'TTL']
dns_request_fields = ['TYPE', 'NAME']

def bad_req(clientAddress):
    msg = "Bad Request".encode('utf-8')
    sock.sendto(msg, clientAddress)

def good_req(clientAddress):
    msg = "Good Request".encode('utf-8')
    sock.sendto(msg, clientAddress)

def response_construction(dic):
    s = ''
    for f in registration_fields:
        s += f + '=' + dic[f] + '\n'
    return s

def dic_construction(ls):
    res = {}
    for s in ls:
        s_splited = s.split('=')
        res[s_splited[0]] = s_splited[1]
    print(res)
    return res 

print("Authorative server initiated")
while True:
    msg, clientAddress = sock.recvfrom(2048)
    print("# UDP msg received")
    msg = msg.decode()
    arg = msg.split('\n')

    # first request validation 
    if len(arg) != 2 and len(arg) != 4:
        msg = "Bad Request".encode('utf-8')
        sock.sendto(msg, clientAddress)

    field_name_storage = set()
    for s in arg:
        if '=' not in s:
            bad_req(clientAddress)
            continue
        s_splited = s.split('=')
        if len(s_splited) != 2:
            bad_req(clientAddress)
            continue
        if len(arg) == 2 and s_splited[0] not in dns_request_fields:
            bad_req(clientAddress)
            continue
        if len(arg) == 4 and s_splited[0] not in registration_fields:
            bad_req(clientAddress)
            continue
        field_name_storage.add(s_splited[0])

    if len(field_name_storage) != len(arg):
        bad_req(clientAddress)
        continue

    arg = dic_construction(arg)

    # get key
    key = arg['NAME'] + ' & ' + arg['TYPE']

    # existence check
    exist = False
    prev = None
    with open(fname, 'r') as json_file:
        data = json.load(json_file)
        if key in data:
            exist = True
        prev = data
    
    # register request
    if len(arg) == 4:
        with open(fname, 'w') as json_file:
            current = prev
            current[key] = arg
            if exist:
                json.dump(prev, json_file)
                bad_req(clientAddress)
            else:
                json.dump(current, json_file)
                good_req(clientAddress)

    # dns request
    else:
        with open(fname, 'r') as json_file:
            data = json.load(json_file)
            if exist:
                dic = data.get(key)
                msg =response_construction(dic)
                print(msg)
                print('-----------')
                sock.sendto(msg.encode(), clientAddress)
            else:
                bad_req(clientAddress)

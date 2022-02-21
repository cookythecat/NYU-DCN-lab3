from flask import Flask, request
import socket
import iptools

app = Flask(__name__)

@app.route("/register", methods = ['PUT'])
def register():
    js_request = request.get_json()
    # json fields validating
    fields = ['hostname', 'ip', 'as_ip', 'as_port']
    for field in fields:
        if field not in js_request:
            return "Some fields are missing", 400
    ip = js_request['ip']
    as_ip = js_request['as_ip']
    as_port = js_request['as_port']
    if not iptools.ipv4.validate_ip(ip):
        return "invalid ip", 400
    if not iptools.ipv4.validate_ip(as_ip):
        return "invalid as_ip", 400 
    if not as_port.isdigit():
        return "invalid port format", 400
    as_port = int(as_port)

    # handle UDP sendding
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3000)
        msg = "TYPE=A\nNAME={}\nVALUE={}\nTTL=10".format(js_request['hostname'], ip)
        print("sending {} to {}:{}".format(msg, as_ip, as_port))
        sock.sendto(msg.encode(), (as_ip, as_port))
        reply, addrr = sock.recvfrom(2048)
        reply = reply.decode()
    except:
        return "UDP request failed", 400
    finally:
        sock.close()

    if reply == "Good Request":
        return "put successful", 201
    else:
        return "bad request, put failed", 400


@app.route("/fibonacci", methods = ['GET'])
def fibonacci():
    arg = request.args
    if 'number' not in arg:
        return 'field number X is neccesary for fibonacci requests', 400
    n = arg['number']
    if not n.isdigit():
        return "number X is not an positive integer", 400
    n = int(n)
    if n < 1:
        return "number X must be greater than 0", 400
    arr = [0] * max((n+1), 3)
    arr[1] = 1
    arr[2] = 1
    for i in range(3, n + 1):
        arr[i] = arr[i - 1] + arr[i - 2]
    return str(arr[n]), 200

app.run(host='0.0.0.0',port=9090, debug=True)
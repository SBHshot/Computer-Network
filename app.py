import sys, getopt
import socket
from youtubesearchpython import VideosSearch

PLAY_HEADER = """\
POST /api/play HTTP/1.1\r
Host: 165.22.48.173:3000\r
\r\n"""

PAUSE_HEADER = """\
POST /api/pause HTTP/1.1\r
Host: 165.22.48.173:3000\r
\r\n"""

NEXT_HEADER = """\
POST /api/next HTTP/1.1\r
Host: 165.22.48.173:3000\r
\r\n"""

VOLUME_HEADER = """\
POST /api/volume HTTP/1.1\r
Host: 165.22.48.173:3000\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: {content_length}\r
Connection: close\r
\r\n"""

ADD_HEADER = """\
POST /api/add HTTP/1.1\r
Host: 165.22.48.173:3000\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: {content_length}\r
Connection: close\r
\r\n"""

target_host = "165.22.48.173"
target_port = 3000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def play():
    client.connect((target_host, target_port))
    header_bytes = PLAY_HEADER.encode('iso-8859-1')
    payload = header_bytes
    client.send(payload)
    response = client.recv(4096)
    print(response.decode().split('\n')[0])
    return

def pause():
    client.connect((target_host, target_port))
    header_bytes = PAUSE_HEADER.encode('iso-8859-1')
    payload = header_bytes
    client.send(payload)
    response = client.recv(4096)
    print(response.decode().split('\n')[0])
    return

def next():
    client.connect((target_host, target_port))
    header_bytes = NEXT_HEADER.encode('iso-8859-1')
    payload = header_bytes
    client.send(payload)
    response = client.recv(4096)
    print(response.decode().split('\n')[0])
    return

def volume(vol):
    if(int(vol) < 1):
        print("Volume must between 1 and 100!")
        sys.exit(2)
    elif(int(vol) > 100):
        print("Volume must between 1 and 100!")
        sys.exit(2)
    client.connect((target_host, target_port))
    body = "volume=" + vol
    body_bytes = body.encode('ascii')
    header_bytes = VOLUME_HEADER.format(
        content_length = len(body_bytes)
    ).encode('iso-8859-1')
    payload = header_bytes + body_bytes
    client.send(payload)
    response = client.recv(4096)
    print(response.decode().split('\n')[0])
    return

def search(query_data):
    video_list = VideosSearch(query_data, limit = 10).result()["result"]
    for video in video_list:
        print(video["id"], video["title"])
    return

def add(id):
    client.connect((target_host, target_port))
    body = "id=" + id
    body_bytes = body.encode('ascii')
    header_bytes = ADD_HEADER.format(
        content_length = len(body_bytes)
    ).encode('iso-8859-1')
    payload = header_bytes + body_bytes
    client.send(payload)
    response = client.recv(4096)
    print(response.decode().split('\n')[0])
    return



def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hpsnv:q:a:", ["volume=", "query=", "add="])
    except getopt.GetoptError:
        print("app.py -p -s -n -v <VOL> -q <QUERY> -a <ID>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("app.py -p -s -n -v <VOL> -q <QUERY> -a <ID>")
            sys.exit()
        elif opt == "-p":
            print("Play")
            play()
            sys.exit()
        elif opt == "-s":
            print("Stop")
            pause()
            sys.exit()
        elif opt == "-n":
            print("Next")
            next()
            sys.exit()
        elif opt == "-v":
            print("Volume Adjust")
            volume(arg)
            sys.exit()
        elif opt == "-q":
            print("Query")
            search(arg)
            sys.exit()
        elif opt == "-a":
            print("Add Video")
            add(arg)
            sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
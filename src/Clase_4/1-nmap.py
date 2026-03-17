import socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(0.5) # tiempo de espera 
    if s.connect_ex(("google.com", 443)) == 0:
        print("puerto abierto")
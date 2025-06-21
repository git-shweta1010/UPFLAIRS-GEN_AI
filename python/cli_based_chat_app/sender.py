import socket 

try:
    ## creating socket//connecting to server
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ##dgram - datagram--network ke trough data transfer
    #  krne k liye
    print("Socket successfully created")
    ip_address = "192.168.1.66"
    port_number =8888                    #0-65536
    target_add = (ip_address, port_number)
    message = input("Enter the message:---> ")
    encripted_messgae = message.encode("ascii")
    s.sendto(encripted_messgae, target_add)

except Exception as msg:
    print(msg)


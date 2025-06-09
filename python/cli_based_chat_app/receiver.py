import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
##sender ke ander hamesha receiver ka ip add dena hai
##reciver me khud ka 
ip_add = "192.168.1.66"
port_number = 8888
complete_add = (ip_add, port_number)
s.bind(complete_add)
while True:
    # message = s.recvfrom(1024)
    # print(message)
    # data = message[0]
    # data = "\n"  #escape characters
    # print(data.encode("ascii"))
    
    # Receive data from sender (max 1024 bytes)
    message, sender_address = s.recvfrom(1024)
    
    print("Raw message:", message)
    print("From:", sender_address)

    # Decode the message to string (if it's in bytes)
    decoded_message = message.decode("utf-8")  # or "ascii" if guaranteed ASCII
    print("Decoded message:", decoded_message)
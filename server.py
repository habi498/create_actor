import socket
import sys 
def onCommand(conn,cmd, text):
    return
def listener(x): 
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 5555        # Port to listen on (non-privileged ports are > 1023)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
        
    print('Socket bind complete')

    #Start listening on socket
    s.listen(5)
    print('Socket now listening')
    #Function for handling connections. This will be used to create threads
           
    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        #conn.send(b'Welcome to the server. Type something and hit enter\n') #send only takes string
        
        #infinite loop so that function do not terminate and thread do not end.
        while True:
            
            #Receiving from client
            data = conn.recv(1024);
            data=data.decode('ascii');
            indx=data.find(" ");
            if(indx==-1):
                onCommand(conn,data,"");
            else:
                r=onCommand(conn,data[:indx],data[indx+1:]);
            if(r!=None):
                conn.send(str(r).encode('ascii'));
            
            if not data: 
                break
        #came out of loop
        conn.close()
        #break;
        print('Connection closed')
    s.close()
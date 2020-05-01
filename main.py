#!/usr/bin/env python3
# importing the threading module 
import threading 
from scapy.all import *
from scapy.utils import rdpcap
import time
import sys
from angle import *
from position import *      
from sequence import * 
import server;
interface='Npcap Loopback Adapter'
#interface='lo'for linux (from command-->ip link show)
#conf.L3socket=L3RawSocket  linux linux linux linux uncomment
def onServerCommand(conn,cmd, text):
    global n;
    global vcmp_port;
    global actors;
    if( cmd == "exit" ):
        sys.exit("exiting...");
    elif( cmd == "print" ):
        print(text);
    elif( cmd == "echo" ):
        conn.send(text.encode('ascii'));
    elif( cmd == "set_actor_pos" ):#SetPos id x y z
        v=text.split(" ");
        actor=actors[(int)(v[0])];
        actor.SetPos((float)(v[1]),(float)(v[2]),(float)(v[3]) );
    elif( cmd=="set_actor_angle"):#set_actor_angle 2.3  -3.14<angle<3.14
        v=text.split(" ");
        actor=actors[(int)(v[0])];
        actor.SetAngle((float)(v[1]));
    elif( cmd == "SetPort" ):
        vcmp_port=(int)(text);
    elif( cmd == "destroy_actor" ):
        actor = actors[(int)(text)];
        name=actor.name;
        if(actor):
            actor.destroy();
            reply = "destroyed "+name;
            conn.send(reply.encode('ascii'));
    elif( cmd == "create_actor" ):#create_actor 3 habi 3.2 5.3 12.3 1.46
        params=text.split(" ");
        a_skin = params[0];
        a_name=params[1];# a means actor
        a_x=(float)(params[2]);
        a_y=(float)(params[3]);
        a_z=(float)(params[4]);
        a_angle=(float)(params[5]);
        port=56327+n+1;
        global guid;
        guid[6:8]=k( h(guid[6:8])+1 , 2 );
        th = threading.Thread(target=create_actor, args=(a_name,port,guid,n,a_x,a_y,a_z,a_angle,a_skin,conn)) 
        n+=1;
        th.start() 
        #create_actor(a_name,port,a_x,a_y,a_z,a_angle);
        return n-1;
    elif( cmd =="get_actor_name" ):
        actor = actors[(int)(text)];
        return actor.name;
    elif( cmd=="set_actor_health"):
        v=text.split(" ");
        actor=actors[(int)(v[0])];
        actor.SetHealth((int)(v[1]));
    elif( cmd =="set_actor_weapon"):
        v=text.split(" ");
        actor=actors[(int)(v[0])];
        actor.SetWeapon((int)(v[1]));
    elif( cmd=="update_action"):
        actor = actors[(int)(text)];
        actor.change_ind+=1;
    elif(cmd=="set_actor_walk_to"):
        v=text.split(" ");
        actor=actors[(int)(v[0])];
        
    elif( cmd =="actor_walk" ):
        v=text.split(" ");
        actor=actors[(int)(v[0])];
        angle=(float)(v[1]);
        actor.angle=angle;#-PI<angle<PI
        y=math.cos(-angle)*2.5;
        x=math.sin(-angle)*2.5;
        z=0;
        message=[147,17]#17 means 0x11
        message[2:]=j("7f ff 71 03 7f ff");
        actor.send(message,32);
        
class Actor:
    ID = None
    x = 0
    y = 0
    z = 0
    angle = 0
    health = 100
    weapon=None
    name=""
    port=None
    octect=0;#0x40=64 for weapon
    pac_seq_no = 10;#next value
    mes_seq_index = 1;#next value
    rel_mes_no = 8;#next value
    ping_packet=None
    change_ind =2;
    def __init__(self, name, port,id):
        self.name = name
        self.port = port
        self.ID = id;
    def SetPos( self, x, y, z ):
        self.x=x;
        self.y=y;
        self.z=z;
        self.Update();
    def SetHealth( self, health ):
        self.health=health;
        self.Update();
    def SetAngle( self, angle ):
        self.angle=angle;
        self.Update();
    def SetWeapon( self, weapon ):
        if(weapon==0):
            self.weapon=None;
        else:
            self.weapon=weapon;
        self.Update();
    def Update( self ):
        if(self.weapon):
            message=[147,64];#0x40
        else:
            message=[147,0];#147 means 0x93
        self.send( message, 32 );
    def send( self, message, reliability ):
        global vcmp_port;
        message_id=message[0];
        c=[132]
        c[1:]=encode_sequence_index(self.pac_seq_no);
        self.pac_seq_no+=1;
        c[4:5]=[reliability];
        c[5:7]=[0,0];#pay_load calculate later.
        if(reliability==32 and message_id==147): #0x20
            c[7:10]=encode_sequence_index(self.mes_seq_index);
            self.mes_seq_index+=1;
            c[10:13]=[2,0,0]#ordering index
            c[13:14]=[0]; #ordering channel
            c[14:15]=[message_id];#0x93
            c[15:19]=k(self.change_ind,4);
            action_seq_index=message[1];
            c[19:20]=[action_seq_index];
            c[20:24]=encode_coordinate(self.x);
            c[24:28]=encode_coordinate(self.y);
            c[28:32]=encode_coordinate(self.z);
            c[32:34]=encode_angle(self.angle);
            if(action_seq_index==0):#00
                c[34:36]=[self.health,3]
            elif(action_seq_index==64):#0x40 weapon
                c[34:37]=[self.weapon,0,20];
                c[37:39]=[self.health,3]
            elif(action_seq_index==17):#0x11
                c[34:40]=message[2:];
                c[40:43]=[0,128,0];#00 0x80 00
                hlt=[self.health,35] #35 is 0x23
                new=split(hlt);#0x64 0x23
                new.insert(0,1);#0x16 42 30
                c[43:]=join(new);
            payload=k( (len(c)-14)*8,2 );
            if(len(payload)==2):
                c[5:7]=payload;
            else:
                c[5:6]=[0];
                c[6:7]=payload #payload length is 1
        elif(reliability==64 and message_id==153):#64 is 0x40, 153 is 0x99
            c[7:10]=encode_sequence_index(self.rel_mes_no);
            self.rel_mes_no+=1;
            c[10:12]=[message_id,1];
            c[5:7]=[0,16]
        p = IP(dst="127.0.0.1")/UDP(sport=self.port,
        dport=vcmp_port)/bytes(c);
        p=IP(raw(p))
        send(p, verbose=True,iface=interface);
        #verbose False means no 'send 1 packet message'
    def destroy(self):
        global actors;
        actors[self.ID]=None;
        self.send([153],64);
    def ping(self): 
        global vcmp_port;
        global actors;
        b=self.ping_packet;
        c = bytearray(b.load);
        c[1:4]=encode_sequence_index(self.pac_seq_no);
        b.load=bytes(c);
        p = IP(dst="127.0.0.1")/UDP(sport=self.port,dport=vcmp_port)/b.load
        p=IP(raw(p))
        send(p, verbose=True,iface=interface);
        self.pac_seq_no+=1;
        if(actors[self.ID]==None):
            return;
        threading.Timer(2.0, self.ping).start()
def create_actor(name,port,gid,id,x,y,z,angle,skin,conn):
    global old_name;
    global pcap_file;
    a=rdpcap(pcap_file)
    i=0;
    b=a[2]
    c=bytearray(b.load);
    c[26:]=gid;
    b.load=bytes(c);
    b=a[3]
    c=bytearray(b.load);
    c[11:19]=guid;
    b.load=bytes(c);
    for b in a:
        m=0;
        if hasattr(b, 'load'):
                index = b.load.find(bytes(old_name.encode()));
                if index >= 0 :
                    c = bytearray(b.load);
                    c[index-1]=len(name);
                    c[6]+=(len(name)-len(old_name))*8
                    b.load=bytes(c);
                    b.load=b.load.replace(bytes(old_name.encode()),bytes(name.encode()))       
        
        if(UDP in b):
            del b[UDP].chksum
            del b[UDP].len
        if(Ether in b and IP in b and UDP in b):
            p = IP(dst="127.0.0.1")/UDP(sport=port,dport=vcmp_port)/b.load
            p=IP(raw(p))
            send(p, verbose=True,iface=interface);
        if(i<len(a)-1):
            m= float( a[i+1].time - a[i].time );
        #time.sleep(m);
        i=i+1;
    bot = Actor(name,port,id);
    global actors;
    actors.append( bot );
    bot.ping_packet=a[8];
    bot.angle=angle;
    bot.SetPos(x,y,z);
    bot.ping();
    reply = "created "+name+" "+str(id)+" "+str(skin);
    conn.send(reply.encode('ascii'));
if __name__ == "__main__": 
    n=0;
    old_name = "habi" #the name with which you recorded
    pcap_file="third.pcap";
    guid=[13, 208, 0, 12, 168, 66, 154, 216]
    vcmp_port=8192
    actors=[];
    server.onCommand=onServerCommand;
    t1 = threading.Thread(target=server.listener, args=(10,)) 
    t1.start() 
#do not use more than one whitespace, in create_actor ...
#it will error.    
        




  

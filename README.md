# create_actor

**Requirements** 
Now it is for Windows only. To adapt it to linux, we need to change Loopback adapter to 'lo'

1.Python 3.7

2.scapy https://github.com/secdev/scapy

3.Npcap Loopback Adapter https://nmap.org/npcap/

**Instructions**

1.Download all the files.
	windows.py ( main file ), 
	server.py, 
	angle.py, 
	position.py,
	sequence.py,
	third.pcap  (pcap file),
	actor.nut (you know where to place this).
  
2.Open command prompt navigate to the directory using cd and type
python windows.py 
and enter. The socket server, which sends packets will start running

3.Now go to your server. I think you must use ysc3839's cmdinput plugin.

Now go to server console( yeah vcmp ) and type

dofile("scripts\actor.nut");

**execute("create_actor 116 lance -661.12 756.365 11.0966 0")**

your first actor is created!

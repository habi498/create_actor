# create_actor

**Requirements** 

Now works in Windows and linux

1.Python 3 or higher

2.scapy https://github.com/secdev/scapy

3.Npcap Loopback Adapter https://nmap.org/npcap/ (for **Windows**)

-------------------------------------------------------------------------------------------------

**Linux**

Install **python 3**. Ubuntu 18.04, it comes with python3 installed

Now you have python3 installed. Install **scapy using pip3 install scapy**

Now you need to find out your **loopback interface**. It is probably 'lo'. Run this cmd ip link show

and find the interface with name "LOOPBACK"

**Windows**

Download and install python 3.8.2 https://www.python.org/downloads/

Install scapy by following instruction on https://scapy.readthedocs.io/en/latest/installation.html#windows. Note we already installed python.

--------------------------------------------------------------------------------------------------------------------

**Instructions for running the program both Windows and Linux**

1.Download all the files.
	main.py ( main file ), 
	server.py, 
	angle.py, 
	position.py,
	sequence.py,
	third.pcap  (pcap file),
	actor.nut (you know where to place this).
	
If you are using **linux**, edit main.py and go to line 13. Comment out line 12. Uncomment line 13 and line 14. So it looks like
```ruby
interface='lo' #we found this in step 3

conf.L3socket=L3RawSocket
```
2.Open command prompt navigate to the directory using cd and type
```ruby
python main.py 
```
and enter. 

Sometimes in **linux**, it might be
```ruby
python3 main.py
```
The socket server, which sends packets will start running

3. Now go to your server. I think you must use ysc3839's cmdinput plugin.

Now go to server console( yeah vcmp ) and type

```ruby
dofile("scripts\actor.nut");
execute("create_actor 116 lance -661.12 756.365 11.0966 0")
```
your first actor is created!

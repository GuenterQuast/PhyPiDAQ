#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" script sendPipe2ws.py
    start script as background process: 
    sendPipe2ws.py [name of pipe] & 

    Read data from a named linux pipe 
    filled by run_phypi.py with option 
    DAQfifo: <name of pipe>
    and send result to websocket on localhost:8314

    read data with script
    readWebsocket.py ws://localhost:8314
"""

import sys, os, errno
import asyncio, websockets

if len(sys.argv)>=2:
  FiFo = sys.argv[1]
else:
  FiFo = "PhyPiDAQ.fifo"
print('*==* ', sys.argv[0], ' Lese Daten aus Pipe',  FiFo)
  
# first, open FiFo to connect to runPhyPiDAQ
#    ignore error if it already exists
try:
  os.mkfifo(FiFo)
except OSError as e:
  if e.errno != errno.EEXIST:
    raise

# set up a websocket for acces via ws://localhost:8314  
# host = 'localhost' only local connections
host=''   # connections from anywhere (if firewall permits)
port = 8314
dbg = False  
async def data_provider(websocket, path):
  async for message in websocket:
    if dbg: print("server got: ", message)

    if message == "req_connect":
    # confirm connection 
      await websocket.send("ack_connect")
    else:
    #  get and send data
      with open(FiFo) as f:
        for inp in f:
          await websocket.send( inp )
          if inp == '\n':
            print("recieved empty input -> end")
            break
      print("end of file reached - closing")
      sys.exit(0)

# start web service 
print('** server running under uri ws://'+host+':', port)
start_server = websockets.serve(data_provider, host, port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()





  
      
      

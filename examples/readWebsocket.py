#!/usr/bin/env python3
"""Read data in CSV format from websocket
"""

import numpy, time
import sys, asyncio
import websockets

# read url from command line
if len(sys.argv)>=2:
  uri = sys.argv[1]
else:
  # host url and port
  uri = "ws://localhost:8314"
print("*==* ", sys.argv[0], " Lese Daten von url ", uri)

async def read_ws():
  """asyncronous read from websocket 
  """    
  async with websockets.connect(uri, ping_interval=None) as websocket:
    # test connection  
    await websocket.send("req_connect")
    answ = await websocket.recv()
    if answ == "ack_connect":
      print("** connected to websocket ", uri)
    
  # get data
    await websocket.send("getData")
    while True:
      inp = await websocket.recv()
      if inp == '\n': # empty record, end
        print("empty input - closing")
        sys.exit(0)
      else:
        print('read: %s '%inp, end='')

# run web client          
asyncio.get_event_loop().run_until_complete(read_ws())

# Jason Brooks
# jaythaceo@gmail.com
# Google: 2016

import re, sys
import struct
from base64 import b64encode
import hashlib

if sys.version_info[0] < 3:
  from SocketServer import ThreadingMixIn, TCPServer, StreamRequestHandler
else:
  from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler


'''
+-+-+-+-+-------+-+-------------+-------------------------------+
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Extended payload length continued, if payload len == 127  |
+ - - - - - - - - - - - - - - - +-------------------------------+
|                     Payload Data continued ...                |
+---------------------------------------------------------------+
'''


FIN    = 0x80
OPCODE = 0x0f
MASKED = 0x80
PAYLOAD_LEN = 0x7f
PAYLOAD_LEN_EXT16 = 0x7e
PAYLOAD_LEN_EXT64 = 0x7f

OPCODE_TEXT = 0x01
CLOSE_CONN  = 0x8


# ----------------------------- API --------------------------------

class API():

  def run_forever(self):
    try:
      print("Listening on port %d for clients.." % self.port)
      self.serve_forever()
    except KeyboardInterrupt:
      self.server_close()
      print("Server terminated")
    except Exception as e:
      print("ERROR: websocketServer: "+str(e))
      exit(1)

  def new_client(self, client, server):
    pass
  def client_left(self, client, server):
    pass
  def message_received(self, client, server, message):
    pass
  def set_fn_new_client(self, fn):
    self.new_client=fn
  def set_fn_client_left(self, fn):
    self.client_left=fn
  def set_fn_message_received(self, fn):
    self.message_received=fn
  def send_message(self, client, msg):
    self._unicast_(client, msg)
  def send_message_to_all(self, msg):
    self,_multicast_(msg)


# --------------------------- Implementation --------------------------

class WebSocketServer(ThreadingMixIn, TCPServer, API):

  allow_reuse_address = True
  daemon_threads = True # comment to keep threads alive until finished

  """
  clients list of a dict:
  {
    'id'      :id
    'handler' :handler
    'address' :(addr, port)
  }

  """
  clients = []
  id_counter = 0

  def __init__(self, port, host='127.0.0.1'):
    self.port = port
    TCPServer.__init__(self, (host, port), WebSocketHandler)














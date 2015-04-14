import argparse
import cocutils
import cocmessages
import cocdecoder
import sys
import re
"""
Tool to unpack a hexadecimal CoC packet according to the specified format, or message id.
"""


parser = argparse.ArgumentParser(description='unpack CoC Messages')
parser.add_argument('--msgid', help='Message ID', type=str)
parser.add_argument('--stmid', help='StreamEntry ID', type=str)
parser.add_argument('--cmdid', help='Command ID', type=str)
parser.add_argument('--format', help='format', type=str)
parser.add_argument('--decoder', help='use decoder', action='store_true')
parser.add_argument('--version', help='Protocol version', type=str)

args= parser.parse_args()

data= sys.stdin.readline().strip().decode("hex")

def parseid(name, names):
    m= re.match(r'^\d+$', name)
    if m:
        return int(m.group(0), 10)
    if not hasattr(names, name):
        return
    return getattr(names, name)

def getformat(name, names, types):
    id= parseid(name, names)
    if id is None:
        return
    if id not in types:
        return
    if "format" not in types[id]:
        return
    return types[id]["format"]


dec= cocdecoder.PacketDecoder()
if args.version:
    dec.version= args.version

if args.decoder:
    if args.msgid:
        msgid= parseid(args.msgid, cocmessages.MSG)
        obj, o= dec.processmessage(msgid, 0, data)
    elif args.stmid:
        stmid= parseid(args.stmid, cocmessages.STM)
        obj, o= dec.decode_StreamMessage(cocutils.packmessage("d", stmid)+data, 0)
    elif args.cmdid:
        cmdid= parseid(args.cmdid, cocmessages.CMD)
        obj, o= dec.decode_Command(cocutils.packmessage("d", cmdid)+data, o)
    else:
        raise Exception("No id specified for decoder")
else:
    fmt= None
    if args.msgid:
        fmt= getformat(args.msgid, cocmessages.MSG, cocmessages.msgtypes)
    elif args.stmid:
        fmt= getformat(args.stmid, cocmessages.STM, cocmessages.stmtypes)
    elif args.cmdid:
        fmt= getformat(args.cmdid, cocmessages.CMD, cocmessages.cmdtypes)
    elif args.format:
        fmt= args.format
    if not fmt:
        raise Exception("No format specified")

    
    fmt= dec.versioned(fmt)

    obj, o= cocutils.unpackobject(fmt, "", data, 0)

cocutils.dumpobj(obj)

if o<len(data):
    print "left: %s" % data[o:].encode("hex")

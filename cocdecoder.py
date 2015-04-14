from cocutils import *
from cocmessages import *
"""
PacketDecoder can be used to print decoded messages: 'display'
or to decode and dispatch using 'processmessage'

"""
class empty:
    pass
class PacketDecoder:
    def decodesimple(self, data, name, decoder):    # cap
        if decoder:
            f, o= unpackmessage(decoder, data)
            print "%s: %s" % (name, f)
        else:
            o= 0
            print "%s" % (name)
        if o<len(data):
            print "WARNING: rest: %s" % (data[o:].encode("hex"))

    def versioned(self, msg):
        if type(msg)==str:
            return msg
        for k,v in msg.items():
            if self.versionmatch(k):
                return v
        print "TODO: scan version list %s  in %s" % (self.version, msg)

    def versionmatch(self, spec):
        if spec==self.version:
            return True
        ix= spec.find("..")
        if ix==0:
            vermin= 0.0
            vermax= float(spec[2:])
        elif ix==len(spec)-2:
            vermin= float(spec[:ix])
            vermax= 99.999
        else:
            vermin= float(spec[:ix])
            vermax= float(spec[ix+2:])
        return vermin <= float(self.version) <= vermax

    def processmessage(self, msgid, unk, data, delegate=None):
        """
        the delegate object can be used to call specific handlers for messages, or commands.
        """
        #print data.encode("hex")
        msgname="?"
        obj= None
        o= 0
        try:
            if msgid in msgtypes:
                msg= msgtypes[msgid]
                msgname= msg["name"]
                #  format  self  delegate
                #    N      N      N   -> print name + hex msg
                #    N      N      Y   -> call delegate with pkt, None
                #    N      Y      N   -> call self with pkt, None
                #    N      Y      Y   -> first call self, then pass result to delegate
                #    Y      N      N   -> simpledecode
                #    Y      N      Y   -> simpledecode + pass result to delegate
                #    Y      Y      N   -> simpledecode + pass result to self
                #    Y      Y      Y

                if "format" in msg:
                    obj, o= unpackobject(self.versioned(msg["format"]), self.versioned(msg.get("fields", "")), data, o)

                if hasattr(self, "decode_"+msg["name"]):
                    obj, o= getattr(self, "decode_"+msg["name"])(data, o, obj)

                if delegate and hasattr(delegate, "handle_"+msg["name"]):
                    getattr(delegate, "handle_"+msg["name"])(data, obj)

                if o==0 and len(data)>0:
                    print "TODO: %s(%d): %s" % (msg["name"], msgid, data.encode("hex"))
                elif o<len(data):
                    print "WARNING: unprocessed(%d): %s" % (msgid, data[o:].encode("hex"))

                if obj:
                    obj.__= msgname

            else:
                print "WARNING: unknown msg: %d: %s" % (msgid, data.encode("hex"))
                obj= None

        except Exception, e:
            print "ERROR: %s: in %s(%d) at offset %d in %s" % (e, msgname, msgid, o, data.encode("hex"))
            #raise

        return obj, o

    def display(self, msgid, obj):
        if not msgid in msgtypes:
            print "WARNING: Strange - unknown msgid(%d) in display" % (msgid)
            return
        msg= msgtypes[msgid]

        if type(obj)==str:
            obj, o= self.processmessage(msgid, 0, obj)

        # todo: handle arrays
        # todo: handle special values, like globalid's
        #     or named constants
        if "display" in msg:
            print "%s %s" % (msg["name"], msg["displayformat"] % getfields(obj, msg["display"]))
        else:
            dumpobj(obj)

    def decode_AvailableServerCommand(self, data, o, obj):
        if not obj: obj= empty()

        obj.cmd, o= self.decode_Command(data, o)
        return obj, o

    def decode_Command(self, data, o):
        hdr, o= unpackmessage("d", data, o)
        cmdid,= hdr

        if cmdid in cmdtypes:
            cmd= cmdtypes[cmdid]
            if "format" in cmd:
                item, o= unpackobject(self.versioned(cmd["format"]), self.versioned(cmd.get("fields", "")), data, o)
            else:
                item= None
            if hasattr(self, "decodecmd_"+cmd["name"]):
                item, o= getattr(self, "decodecmd_"+cmd["name"])(data, o, item)
#               if delegate and hasattr(delegate, "handlecmd_"+cmd["name"]):
#                   getattr(delegate, "handlecmd_"+cmd["name"])(data, item)

            item.__= cmd["name"]
            return item, o
        else:
            print "WARNING: unknown cmd: %d: %s" % (cmdid, data[o:].encode("hex"))
        return None, o

    def decode_EndClientTurn(self, data, o, obj):
        o=0
        """
        hdr:
        0: d  time in 1/60 seconds since login
        1: d  checksum
        2: d  nr of actions

        when hdr[1] has the wrong value, the server responds with a 'OutOfSync' message
        containing the right value.
        """
        ahdr, o= unpackmessage("ddd", data, o)


        curtick, checksum, nractions= ahdr


        obj= empty()
        obj.curtick= curtick
        obj.checksum= checksum
        obj.cmds=[]

        count= 0
        while o<len(data) and count<nractions:
            item, o= self.decode_Command(data, o)

            if not item:
                break

            obj.cmds.append(item)

            count += 1

        if count!=nractions:
            print "WARNING: Too few Actions(%d), expected(%d)" % (count, nractions)
        return obj, o

    def decode_AllianceStreamMessage(self, data, o):
        hdr, o= unpackmessage("d", data, o)
        stmid,= hdr

        if stmid in lstmtypes:
            stm= lstmtypes[stmid]
            if "format" in stm:
                #print "%d: %s   %s" % (stmid, stm["format"], data[o:].encode("hex"))
                item, o= unpackobject(self.versioned(stm["format"]), self.versioned(stm.get("fields", "")), data, o)
            else:
                item= None
            if hasattr(self, "decodestm_"+stm["name"]):
                item, o= getattr(self, "decodestm_"+stm["name"])(data, o, item)
#               if delegate and hasattr(delegate, "handlestm_"+stm["name"]):
#                   getattr(delegate, "handlestm_"+stm["name"])(data, item)

            item.__= stm["name"]
            return item, o
        else:
            print "WARNING: unknown lstm: %d: %s" % (stmid, data[o:].encode("hex"))
        return None, o



    def decode_AllianceStream(self, data, o, obj):
        hdr, o= unpackmessage("d", data, o)
        nrmsgs,= hdr

        obj= empty()
        obj.msgs=[]

        count= 0
        while o<len(data) and count<nrmsgs:
            item, o= self.decode_AllianceStreamMessage(data, o)

            if not item:
                break

            obj.msgs.append(item)

            count += 1

        if count!=nrmsgs:
            print "WARNING: Too few Messages(%d), expected(%d)" % (count, nrmsgs)
        return obj, o

    def decode_AvatarStreamMessage(self, data, o):
        hdr, o= unpackmessage("d", data, o)
        stmid,= hdr

        if stmid in vstmtypes:
            stm= vstmtypes[stmid]
            if "format" in stm:
                #print "%d: %s   %s" % (stmid, stm["format"], data[o:].encode("hex"))
                item, o= unpackobject(self.versioned(stm["format"]), self.versioned(stm.get("fields", "")), data, o)
            else:
                item= None
            if hasattr(self, "decodestm_"+stm["name"]):
                item, o= getattr(self, "decodestm_"+stm["name"])(data, o, item)
#               if delegate and hasattr(delegate, "handlestm_"+stm["name"]):
#                   getattr(delegate, "handlestm_"+stm["name"])(data, item)

            item.__= stm["name"]
            return item, o
        else:
            print "WARNING: unknown vstm: %d: %s" % (stmid, data[o:].encode("hex"))
        return None, o

    def decode_AvatarStream(self, data, o, obj):
        hdr, o= unpackmessage("d", data, o)
        nrmsgs,= hdr

        obj= empty()
        obj.msgs=[]

        count= 0
        while o<len(data) and count<nrmsgs:
            item, o= self.decode_AvatarStreamMessage(data, o)

            if not item:
                break

            obj.msgs.append(item)

            count += 1

        if count!=nrmsgs:
            print "WARNING: Too few Messages(%d), expected(%d)" % (count, nrmsgs)
        return obj, o



    def decodecmd_BuyResources(self, data, o, obj):
        if not obj: obj= empty()

        obj.cmd, o= self.decode_Command(data, o)

        (obj.cmdtick,), o= unpackmessage("d", data, o)

        return obj, o


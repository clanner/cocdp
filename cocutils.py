import struct
import zlib
import json
"""
Collection of functions used in decoding the CoC protocol

 * newscramble   - the scramble function used by CoC v7.x
 * scramble      - the scramble function used by CoC v6.x

 * packmessage + unpackmessage  - pack/unpack string based on a simple format specification
      's'  - string   ( prefixed with 32 bit size )
      'b'  - byte
      'h'  - halfword ( 16 bit )
      'd'  - dword    ( 32 bit )
      'q'  - quadword ( 64 bit )
 
 * unpackobject  - like unpackmessage, but returns object with named attributes,
                   and supports simple nested structures
      '#[...]' - array
      '?(...)' - optional   ( prefixed with boolean byte )
      '={...}' - struct

   note that consequetive 'false' values are coalesced into one byte.

"""
class empty:
    pass

def lshift(num, n):
    return (num*(2**n))%(2**32)
def rshift(num, n):
    highbits= 0
    if num&(2**31):
        highbits= (2**n-1)*(2**(32-n))
    return (num/(2**n))|highbits
def isneg(num):
    return num&(2**31)
def negate(num):
    return (~num)+1
class prng:
    def __init__(self, seed):
        self.seed= seed
    def next(self):
        v3= self.seed if self.seed else 0xffffffff

        v3 ^= lshift(v3,13)
        v3 ^= rshift(v3,17)
        v3 ^= lshift(v3,5)

        self.seed= v3
        if isneg(v3):
            v3= negate(v3)
        return v3%0x100

def scramble(data, seed):
    rng= prng(seed)
    return "".join(chr(ord(c)^rng.next()) for c in data)

class scramble7prng:
    def __init__(self, seed):
        self.ix= 0
        self.buffer= [ 0 for i in range(624) ]
        self.seedbuffer(seed)
    def dumpbuffer(self):
        for x in self.buffer:
            print " %08x" % x,
        print
    def seedbuffer(self, seed):
        for i in range(624):
            self.buffer[i]= seed
            seed= (1812433253 * ((seed ^ rshift(seed, 30)) + 1)) & 0xFFFFFFFF
    def getbyte(self):
        x= self.getint()
        if isneg(x):
            x= negate(x)
        return x % 256
    def getint(self):
        if self.ix==0:
            self.mixbuffer()
        val= self.buffer[self.ix]
        self.ix = (self.ix+1) % 624

        val ^= rshift(val, 11) ^ lshift((val ^ rshift(val, 11)), 7) & 0x9D2C5680;
        return rshift((val ^ lshift(val, 15) & 0xEFC60000), 18) ^ val ^ lshift(val, 15) & 0xEFC60000;
    def mixbuffer(self):
        i=0
        j=0
        while i<624:
            i += 1
            v4= (self.buffer[i%624] & 0x7FFFFFFF) + (self.buffer[j]&0x80000000)
            v6 = rshift(v4,1) ^ self.buffer[(i+396)%624]
            if v4&1:
                v6 ^= 0x9908B0DF
            self.buffer[j] = v6
            j += 1


def newscramble(serverrandom, seed):
    prng= scramble7prng(seed)
    for i in range(100):
        byte100= prng.getbyte()
    return "".join(chr(ord(c)^(prng.getbyte()&byte100)) for c in serverrandom)



def getqword(data, ofs):
    return struct.unpack(">Q", data[ofs:ofs+8])[0], ofs+8
def getdword(data, ofs):
    return struct.unpack(">L", data[ofs:ofs+4])[0], ofs+4
def gethword(data, ofs):
    return struct.unpack(">H", data[ofs:ofs+2])[0], ofs+2
def getbyte(data, ofs):
    return struct.unpack(">B", data[ofs:ofs+1])[0], ofs+1

def getstring(data, ofs):
    slen, ofs= getdword(data, ofs)
    if slen==0xFFFFFFFF:
        return None, ofs
    if ofs+slen>len(data):
        raise Exception("string length exceeds data length: %08x" % slen)
    return data[ofs:ofs+slen], ofs+slen
def unpackmessage(fmt, data, o=0):
    """
    unpack string based on format specified in 'fmt'
    """
    lst=[]
    for t in fmt:
        if t=="s":
            val, o= getstring(data, o)
        elif t=="q":
            val, o= getqword(data, o)
        elif t=="d":
            val, o= getdword(data, o)
        elif t=="h":
            val, o= gethword(data, o)
        elif t=="b":
            val, o= getbyte(data, o)
        else:
            raise Exception("unksupported format: %s" % t)
        lst.append(val)
    return lst, o


def makebyte(x):
    return struct.pack(">B", x)
def makehword(x):
    return struct.pack(">H", x)
def makedword(x):
    return struct.pack(">L", x)
def makeqword(x):
    return struct.pack(">Q", x)
def makestring(str):
    if str == None:
        return makedword(0xFFFFFFFF)
    return makedword(len(str))+str
def packmessage(fmt, items):
    """
    create string based on format specified in 'fmt'
    """
    data= ""
    for t,item in zip(fmt, items):
        print "-- %s: %s: %s" % (t, type(item), item)
        if t=="s":
            data += makestring(item)
        elif t=="d":
            data += makedword(item)
        elif t=="q":
            data += makeqword(item)
        elif t=="h":
            data += makehword(item)
        elif t=="b":
            data += makebyte(item)
        else:
            raise Exception("unksupported format: %s" % t)
    return data


# unpack more complex formats
# adding:
#    array:    #[...]
#    optional: ?(...)
#    struct:   ={...}
#

# fields contains a list of names, or '?'
# optionals are encoded as  'name(...)'
# arrays are encoded as 'name[...]'
# structs are encoded as 'name{...}'


# get bracketed subformat
#   not handling nested formats.
def subformat(fmt, i):
    if i>=len(fmt):
        return ""
#    j= fmt.index(']', i)
#    print "FMT: <%s / %s / %s / %s / %s>" % ( fmt[:i], fmt[i], fmt[i+1:j], fmt[j], fmt[j+1:])
    if fmt[i]=='[':
        return fmt[i+1:fmt.index(']', i)]
    if fmt[i]=='(':
        return fmt[i+1:fmt.index(')', i)]
    if fmt[i]=='{':
        return fmt[i+1:fmt.index('}', i)]
    raise Exception("expected subformat: %s, ofs %d" % (fmt, i))

def getfieldname(fields, i):
    if i>=len(fields):
        return "?"
    iend= fields.find(' ', i)
    if iend==-1:
        return fields[i:]
    else:
        return fields[i:iend]

def unpackobject(fmt, fields, data, o=0):
    """
    create object with attributes specified in 'fields' and format specified in 'fmt'
    """
    obj= empty()
    ifmt= 0
    ifield= 0
    itemnr= 0
    bitfield= None
    bitmask= 0

    while ifmt<len(fmt):
      try:
        t= fmt[ifmt]
        ifmt += 1
        fn= getfieldname(fields, ifield)
        ifield += len(fn)+1

        #print "%-10s %s" % (t, fn)
        if fn=="?":
            fn= "field_%02d" % (itemnr)

        keepbitfield= False

        if t=="s":
            val, o= getstring(data, o)
        elif t=="q":
            val, o= getqword(data, o)
        elif t=="d":
            val, o= getdword(data, o)
        elif t=="h":
            val, o= gethword(data, o)
        elif t=="b":
            val, o= getbyte(data, o)
        elif t=="?":
            sfmt= subformat(fmt, ifmt)
            ifmt += len(sfmt)+2
            sfld= subformat(fields, ifield)
            ifield += len(sfld)+3

            #print "fmt: '%s'  .. '%s'" % (sfmt, fmt[ifmt:])
            #print "flp: '%s'  .. '%s'" % (sfld, fields[ifield:])

            if bitfield is None:
                bitfield, o= getbyte(data, o)
                bitmask= 1
            else:
                bitmask *= 2
            if bitfield & bitmask:
                val, o= unpackobject(sfmt, sfld, data, o)
            else:
                keepbitfield= True
                val= None
        elif t=="=":
            sfmt= subformat(fmt, ifmt)
            ifmt += len(sfmt)+2
            sfld= subformat(fields, ifield)
            ifield += len(sfld)+3

            val, o= unpackobject(sfmt, sfld, data, o)
        elif t=="#":
            sfmt= subformat(fmt, ifmt)
            ifmt += len(sfmt)+2
            sfld= subformat(fields, ifield)
            ifield += len(sfld)+3

            #print "#: '%s'  '%s'" % (sfmt, sfld)
            count, o= getdword(data, o)
            val= []
            for i in xrange(count):
                item, o= unpackobject(sfmt, sfld, data, o)
                val.append(item)
        else:
            raise Exception("unksupported format: %s" % t)
        if not keepbitfield:
            bitfield= None
        #print "%d: %d/%d: %s %s\t%s" % (itemnr, ifmt, ifield, t, fn, val)
        if not hasattr(obj, '__fields'):
            obj.__fields = []
        obj.__fields.append(fn)
        setattr(obj, fn, val)
        itemnr += 1
      except Exception, e:
        print "fmt: %d of %s" % (ifmt, fmt)
        print "EXCEPTION %s: at %d" % (e, o)
        raise

#   if ifmt<len(fmt) or ifield<len(fields):
#       print "WARNING: format(%d<%d)/field(%d<%d) mismatch" % (ifmt, len(fmt), ifield, len(fields))
#       print "fmt='%s'" % fmt
#       print "fld='%s'" % fields

    return obj, o


# "field_1.field_2"  returns obj.field_1.field_2
# todo: add support for arrays
def getfield(obj, spec):
    i= spec.find('.')
    if i==-1:
        return getattr(obj, spec)
    obj= getattr(obj, spec[:i])
    if obj:
        return getfield(obj, spec[i+1:])
    else:
        return None

def getfields(obj, flist):
    return tuple(getfield(obj, spec) for spec in flist.split(' '))

def dumpobj(obj, l=1):
    """
    recursively pretty print contents of a python object.
    """
    if hasattr(obj, '__'):
        print "%s%s" % ("  " * l, obj.__)
    if hasattr(obj, '__fields'):
        fields = obj.__fields
    else:
        fields = vars(obj).keys()
    for k in fields:
        v = getattr(obj, k)
        if type(v)==type(obj):
            print "%s%s: {" % ("  " * l, k)
            dumpobj(v, l+1)
            print "%s}" % ("  " * l)
        elif type(v)==type([]):
            print "%s%s: [" % ("  " * l, k)
            for i in range(len(v)):
                if type(v[i])==type(obj) and len(vars(v[i]).items()) > 1 or type(v[i])==type([]) and len(v[i]) > 0:
                    print "%s[%d]=\n" % ("  " * (l+1), i),
                    dumpobj(v[i], l+2)
                else:
                    print "%s[%d]=" % ("  " * (l+1), i),
                    dumpobj(v[i], 0)
            print "%s]" % ("  " * l)
        elif type(v)==str:
            if v[3:6]=="\x00\x78\x9c":
                fullsize,= struct.unpack("<L", v[0:4])
                compdata= v[4:]
                v= zlib.decompress(compdata, 15, fullsize)
                if v[0] == '{':
                    v = json.dumps(json.loads(v), indent=4)
                    v = ("  " * l).join(v.splitlines(True))
            print "%s%s: \"%s\"" % ("  " * l, k, v)
        elif type(v)==int:
            if v>1000000 and (v%1000000)<1000:
                # print resource id's as decimal
                print "%s%s: %d" % ("  " * l, k, v)
            else:
                if v == 0:
                    print "%s%s: 0x%x" % ("  " * l, k, v)
                else:
                    print "%s%s: 0x%x (%d)" % ("  " * l, k, v, v)
        else:
            print "%s%s: %s" % ("  " * l, k, v)



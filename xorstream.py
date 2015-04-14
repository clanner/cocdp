import sys
import rc4
import cocutils
import argparse

"""
xorstream generates the first 512 bytes of the CoC xor stream.

Without arguments the initial xor bytes are generated.
With --seed + --key you can calculate the xor bytes after the Login+Encryption packets
were exchanged.

"""
rc4key="fhsd6f86f67rt8fw78fw789we78r9789wer6re"
nonce= "nonce"

parser = argparse.ArgumentParser(description='generate CoC xor stream')
parser.add_argument('--v7',  action='store_true', help='use v7 scramble')
parser.add_argument('--seed', type=str, metavar='SEED', help='the client seed')
parser.add_argument('--key', type=str, metavar='KEY', help='the server random')
parser.add_argument('--nonce', type=str, metavar='KEY', help='the scrambled server random')

args = parser.parse_args()

def makerc4(nonce):
    rc= rc4.RC4(rc4key+nonce)
    # skip keylen bytes
    for i in range(len(rc4key)+len(nonce)):
        rc.next()
    return rc

if args.key:
    clientseed= int(args.seed, 0)
    svrrandom= args.key.decode("hex")
    if args.v7:
        nonce= cocutils.newscramble(svrrandom, clientseed)
    else:
        nonce= cocutils.scramble(svrrandom, clientseed)
elif args.nonce:
    nonce= args.nonce.decode("hex")

print "nonce=%s" % nonce.encode("hex")
rc= makerc4(nonce)
for i in range(512):
    print "%02x" % rc.next(),
    if (i%32)==31:
        print


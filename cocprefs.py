from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import argparse
import sys
from base64 import b64encode, b64decode
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape as xml_escape
from xml.sax.saxutils import unescape as xml_unescape

"""
Tool for decoding or updating these configuration files:
/data/data/com.supercell.clashofclans/shared_prefs/localPrefs.xml
/data/data/com.supercell.clashofclans/shared_prefs/storage.xml

The android id can be found in openudid_prefs.xml
or in adb shell:  settings get secure android_id

decoding:
    python cocprefs.py --from YOURANDROIDID  storage.xml

-> will print the decrypted config file

converting
    python cocprefs.py --from YOURANDROIDID --to OTHERANDROIDID storage.xml

-> will print the config file, converted for your OTHERANDROIDID device

encoding
    python cocprefs.py --to YOURANDROIDID  storage.xml

-> will print the encrypted config for storage.xml



You will have to use adb on a rooted device to get the storage files from the device yourself.
"""


""" ====================================================================== """
def makekeycipher(key):
    hashedkey= SHA256.new(key).digest()

    return AES.new(hashedkey, AES.MODE_ECB)

def makevalcipher(key):
    hashedkey= SHA256.new(key).digest()

    return AES.new(hashedkey, AES.MODE_CBC, "fldsjfodasjifuds")


""" ====================================================================== """
def parse_xml(xml):
    """ convert xml to config dict """

    d={}
    root= ET.fromstring(xml)
    # root.tag=="map"
    for line in list(root):
        # line.tag=="string"
        k= line.attrib["name"]
        v= line.text
        d[k]= v

    return d

def create_xml(cfg):
    """ convert config dict to xml """
    xml= "<?xml version='1.0' encoding='utf-8' standalone='yes' ?>\n"
    xml += "<map>\n"
    for k,v in cfg.items():
        xml += "    <string name=\"%s\">%s</string>\n" % (xml_escape(k), xml_escape(v))
    xml += "</map>\n"

    return xml

""" ====================================================================== """
def pkcs5_pad(s):
    BLOCK_SIZE= 16
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

def pkcs5_unpad(s):
    return s[0:-ord(s[-1])]
 

""" ====================================================================== """
def decrypt(value, cipher):
    return pkcs5_unpad(cipher.decrypt(b64decode(value)))
def encrypt(value, cipher):
    return b64encode(cipher.encrypt(pkcs5_pad(value)))

""" ====================================================================== """
def decode_xml(xml, key):
    """ decrypted xml config to config dict """
    enc= parse_xml(xml)
    if key is None:
        return enc

    dec= {}

    keycipher= makekeycipher(key)
    for k, v in enc.items():
        valcipher= makevalcipher(key)
        dec[decrypt(k, keycipher)]= decrypt(v, valcipher)

    return dec

def encode_xml(cfg, key):
    """ convert config dict to encrypted xml """
    if key is None:
        return create_xml(cfg)

    enc= {}

    keycipher= makekeycipher(key)
    for k, v in cfg.items():
        valcipher= makevalcipher(key)
        enc[encrypt(k, keycipher)]= encrypt(v, valcipher)

    return create_xml(enc)


""" ====================================================================== """
def handle_fh(fh, args):
    xml= fh.read()
    cfg= decode_xml(xml, args.from_)
    print encode_xml(cfg, args.to)

def handle_xmlfile(fn, args):
    with open(fn) as fh:
        handle_fh(fh, args)

""" ====================================================================== """
parser = argparse.ArgumentParser(description='Clash-of-Clans configuration editor')
parser.add_argument("--from", dest='from_', type=str, help="source android_id")
parser.add_argument("--to", type=str, help="target android_id")
parser.add_argument("xmlfiles", type=str, metavar="XML", nargs="*", help="a xml config file")

args = parser.parse_args()

if not args.xmlfiles:
    handle_fh(sys.stdin, args)
else:
    for fn in args.xmlfiles:
        handle_xmlfile(fn, args)


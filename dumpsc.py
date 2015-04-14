import sys
import struct
import PIL.Image
import os.path
import argparse

"""
Tool for extracting ClashOfClans .sc files


Note: first decompress the .sc files using 'decompress_csv.py'

find assets -name "*.sc" | while read f; do
    echo ========= $f
    python dumpsc.py $f
done


01 : bitmaps
  (t, w, h)= "BHH" 

  t=00: 32bit color
  t=02: 16bit color

07 : strings 'CCBackBeat', 'Supercell-Magic'
0f : strings 'Arial' 'Berlin Sans FB Demi' 'CCBackBeat' 'Squarejaw Intl BB' 'Supercell-Magic'

09 : 7 bytes
08 :24 bytes

0c : contains many texts

12 : <BBHH
       followed by  '11' type records  - polygons
11 : BB,  ? + pathlen, followed by 8*len bytes, then len points

  extract poly:
     - calc boundingbox for poly
     - create bitmap for bb
     - clear all pixels outside of poly

"""

def createmask(path):
    bb= path.getbbox()
    bbsize= (abs(bb[2]-bb[0]), abs(bb[3]-bb[1]))
    img= PIL.Image.new("1", bbsize)
    draw= PIL.ImageDraw.Draw(img)

    draw.polygon(path, fill=1)

    return img

def extractimg(im, poly):
    path= PIL.ImagePath.Path(poly)
    bb= path.getbbox()
    bbsize= (abs(bb[2]-bb[0]), abs(bb[3]-bb[1]))
    tx= PIL.ImageTransform.ExtentTransform(path.getbbox())

    newimg= im.transform(bbsize, tx)

    # update path to match 'newimg'
    path.map(lambda x,y:(x-bb[0], y-bb[1]))

    # now clear pixels outside poly

    img= PIL.Image.new("RGBA", bbsize)
    img.paste(newimg, createmask(path))

    return img

def unpackstr(data, o):
    l,= struct.unpack_from("B", data, o)
    o += 1
    return data[o:o+l], o+l

def convertpixel(px, t):
    if t==4:
        x,= struct.unpack("<H", px)
        return (((x>>11)&31)<<3, ((x>>5)&63)<<2, (x&31)<<3)
    elif t==0:
        r,g,b,a = struct.unpack("4B", px)
        return (r,g,b,a)
    elif t==2:
        x,= struct.unpack("<H", px)
        r,g,b,a= ( ((x>>12)&15)<<4, ((x>>8)&15)<<4, ((x>>4)&15)<<4, ((x>>0)&15)<<4) 

        return (r,g,b,a)
    else:
        raise Exception("unknown pixel type")

def save_bitmap(w, h, pixelsize, bmt, bmp, fn):
    img= PIL.Image.new("RGBA", (w,h))
    pixels= []
    for o in range(0,len(bmp),pixelsize):
        pixels.append(convertpixel(bmp[o:o+pixelsize], bmt))
    img.putdata(pixels)
    img.save(fn, "PNG")

def process_sc(data, basename, savedir):
    o= 0
    h= struct.unpack_from("<6H5sH", data, o)
    o += 19
    nr= h[-1]
    ofslist= struct.unpack_from("<%dH" % nr, data, o)
    o += 2*nr
    strlist= []
    for i in xrange(nr):
        print "%s  %d" % (basename, i)
        s, o= unpackstr(data, o)
        strlist.append(s)
    d= {}
    i= 0
    while o+5<=len(data):
        t, l= struct.unpack_from("<BL", data, o)
        o += 5
        if t==0 and l==0:
            break
        if t not in d:
            d[t]= 0
        d[t] += 1

        if t==1:
            bmt,bmw,bmh= struct.unpack_from("<BHH", data, o)
            if bmt==0:
                pixelsize=4
            elif bmt==2:
                pixelsize=2
            elif bmt==4:
                pixelsize=2
            else:
                print "unknown pixeltype: %d" % (bmt)

            bmpsize= bmw*bmh*pixelsize

            if savedir:
                save_bitmap(bmw, bmh, pixelsize, bmt, data[o+5:o+5+bmpsize], "%s/%s-%d.png" % (savedir, basename, bmt))

            i += 1

            print "=%02x=%02x  %d x %d   .. bmpsize=%x, left=%x" % (t, bmt, bmw, bmh, bmpsize, l-bmpsize-5)
        else:
            print "=%02x=%s" % (t, data[o:o+l].encode("hex"))
        o += l
    if o<len(data):
        print "leftover: %s" % data[o:].encode("hex")

    print "%5d , %5d: 12"                 % (h[0], d.pop(18, 0))
    print "%5d , %5d: 0c"                 % (h[1], d.pop(12, 0))
    print "%5d , %5d: 01    - bitmaps"    % (h[2], d.pop(1, 0))
    print "%5d , %5d: 07/0f"              % (h[3], d.pop(7, 0)+d.pop(15, 0))
    print "%5d , %5d: 08"                 % (h[4], d.pop(8, 0))
    print "%5d , %5d: 09"                 % (h[5], d.pop(9, 0))

    for t in d:
        print "        %5d: %02x" % (d[t], t)
    if h[6] != "\x00" * 5:
        print "h6: %s" % h[6].encode("hex")

    for i in xrange(nr):
        print " * %5d: %04x '%s'" % (i, ofslist[i], strlist[i])


parser = argparse.ArgumentParser(description='Print information, or extract bitmaps from CoC (decompressed) .sc files')
parser.add_argument('--extract', help='Extract bitmaps to directory', type=str)
parser.add_argument('files', help='sc file', nargs='+')

args = parser.parse_args()

for fn in args.files:
    basename, rest= os.path.splitext(os.path.basename(fn))
    with open(fn) as fh:
        data= fh.read()
        process_sc(data, basename, args.extract)


import lzmaffi as lzma
import sys

"""
find . -name "*.csv" | xargs python decompress_csv.py

Will print all decompressed csv files.
"""

n=len(sys.argv)
for fn in sys.argv[1:]:
    try:
        with open(fn) as fh:
            lz=lzma.LZMADecompressor()
            data=fh.read()
            data=data[0:9]+("\x00" * 4)+data[9:]
            if n>2:
                print "==> %s <==" % (fn)
            sys.stdout.write(lz.decompress(data))
            if n>2:
                print
                print
    except:
        e = sys.exc_info()[0]
        print "<p>Error: %s</p>" % e


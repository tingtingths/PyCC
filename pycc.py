# Chinese characters convert tool
# Traditional <--> Simplified, from any encoding to utf-8.
import sys
import chardet
import os
import glob
import argparse
from collections import deque


def detect(bytes):
    encoding_swap = {"big5":"cp950", "gb2312":"gbk"}
    codec = chardet.detect(bytes)["encoding"]
    if codec == None:
        return None
    return codec if codec.lower() not in encoding_swap else encoding_swap[codec.lower()]


def convert(s, d):
    new_s = ""

    for c in s:
        if c in d:
            c = d[c]
        new_s += str(c)

    return new_s


def construct_dict(filename):
    d = {}

    with open(filename, "r", encoding="utf8") as f:
        for line in f:
            lst = line.split("-")
            d[lst[0]] = lst[1].rstrip().split(".")[0]

    return d

def convert_files(d, files, dry_run=False):
    for f in files:
        org_f = open(f, "rb")
        org_filename = os.path.basename(org_f.name)
        org_dirname = os.path.dirname(os.path.abspath(org_f.name))
        codec = detect(org_f.read())
        print(f)
        if codec == None:
            codec = input("Error detecting encoding, set encoding to >")
            print("    Selected encoding: " + codec)
        else:
            print("    Suggested encoding: " + codec)
        if not dry_run:
            s = convert(open(f, encoding=codec).read(), d)
            open(org_dirname + os.path.sep + "_" + org_filename, "w", encoding="utf8").write(s)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert chinese characters.")
    parser.add_argument("-t", choices=["s2t", "t2s"], help="simplified chinese to traditional chines or vice versa")
    parser.add_argument("--dry-run", action="store_true", help="print detected encoding only")
    parser.add_argument("-s", metavar="string", type=str, nargs="*", help="string(s) to convert")
    parser.add_argument("-f", metavar="file", type=str, nargs="*", help="file(s) to convert")
    args = parser.parse_args()

    cd = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "dict" + os.path.sep
    dict = construct_dict(cd + args.t)
    if args.f:
        convert_files(dict, args.f, args.dry_run)
    if args.s:
        for s in args.s:
            convert(dict, s, construct_dict(cd + command))

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

def convert_files(d, files, dry_run=False, replace=False):
    for f in files:
        org_f = open(f, "rb")
        org_filename = os.path.basename(org_f.name)
        org_dirname = os.path.dirname(os.path.abspath(org_f.name))
        codec = detect(org_f.read())
        print(f)
        if codec == None and not dry_run:
            codec = input("Error detecting encoding, set encoding to >")
            print("    Selected encoding: " + codec)
        else:
            print("    Detected encoding: " + codec)
        if not dry_run:
            s = convert(open(f, encoding=codec).read(), d)
            prefix = "" if replace else "_"
            open(org_dirname + os.path.sep + prefix + org_filename, "w", encoding="utf8").write(s)

def convert_strings(d, strings, dry_run=False):
    for s in strings:
        codec = detect(s.encode())
        print(s)
        if codec == None and not dry_run:
            codec = input("Error detecting encoding, set encoding to >")
            print("    Selected encoding: " + codec)
        else:
            print("    Detected encoding: " + codec)
        if not dry_run:
            print(convert(s, d))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert chinese characters.")
    parser.add_argument("operation", choices=["s2t", "t2s"], help="simplified chinese to traditional chines or vice versa")
    parser.add_argument("--dry-run", action="store_true", help="print detected encoding only")
    parser.add_argument("--replace", action="store_true", help="replace original file(s)")
    parser.add_argument("inputs", metavar="INPUT", type=str, nargs="+", help="file(s) or string(s) to convert")
    args = parser.parse_args()

    cd = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "dict" + os.path.sep
    if not args.dry_run:
        dict = construct_dict(cd + args.operation)
    for _input in args.inputs:
        files = []
        strings = []
        if os.path.exists(_input):
            files.append(_input)
        else:
            strings.append(_input)

        convert_files(dict, files, args.dry_run, args.replace)
        convert_strings(dict, strings, args.dry_run)

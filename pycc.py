# Chinese characters convert tool
# Traditional <--> Simplified, from any encoding to utf-8.
import sys
import chardet
import os
import glob
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


def convert_files(d, files):
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
        s = convert(open(f, encoding=codec).read(), d)
        open(org_dirname + os.path.sep + "_" + org_filename,
            "w", encoding="utf8").write(s)


def print_help():
    print("Usage: " + os.path.basename(__file__) + " <command> [option] <input_file | glob_pattern | string>...")
    print("  command:")
    print("    -t2s         Traditional chinese to Simplified chinese")
    print("    -s2t         Simplified chinese to Traditional chinese")
    print("    -i           Only print suggested encoding for file(s)")
    print("  option:")
    print("    -g           Select file(s) with glob pattern")
    print("    -s           Convert using string(s) from argument")

if __name__ == "__main__":
    args = deque(sys.argv[1:])

    if len(sys.argv) < 2 or "-h" in args or "-help" in args:
        print_help()
    else:
        try:
            command = args.popleft()[1:]
            input_string = False
            if "-g" == args[0]:
                args.popleft()
                input = glob.glob(args.popleft())
            elif "-s" == args[0]:
                args.popleft()
                input_string = True
                input = args
            else:
                input = args
            cd = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "dict" + os.path.sep
            if command == "i":
                for f in input:
                    print("Suggested encoding:" + detect(open(f, "rb").read()))
            elif command == "t2s" or command == "s2t":
                if input_string:
                    for s in args:
                        print(convert(s, construct_dict(cd + command)))
                else:
                    convert_files(construct_dict(cd + command), input)
            else:
                print_help()
        except Exception as e:
            print(e)

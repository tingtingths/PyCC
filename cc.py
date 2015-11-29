# Chinese characters convert tool
# Traditional <--> Simplified, from any encoding to utf-8.
import sys, chardet, os


def detect(bytes):
    return chardet.detect(bytes)["encoding"]


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
        encoding = detect(open(f, "rb").read())
        print("Suggested encoding:" + encoding)
        s = convert(open(f, "r", encoding=encoding).read(), d)
        open("_" + f, "w", encoding="utf8").write(s)

if __name__ == "__main__":

    if len(sys.argv) < 3:
        # display help
        print("Usage: cc <option = -t2s/-s2t/-i> <input files>")

    if len(sys.argv) >= 3:
        files = sys.argv[2:]
        option = sys.argv[1]
        cd = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "dict" + os.path.sep

        if option == "-t2s":
            dict_file = "t2s"
            convert_files(construct_dict(cd + dict_file), files)
        elif option == "-s2t":
            dict_file = "s2t"
            convert_files(construct_dict(cd + dict_file), files)
        elif option == "-i":
            for f in files:
                print("Suggested encoding:" + detect(open(f, "rb").read()))
        else:
            print("Usage: cc <option = -t2s/-s2t/-i> <input files>")

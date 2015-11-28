# Chinese characters convert tool
# Traditional <--> Simplified, from any encoding to utf-8.
import sys, chardet


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

if __name__ == "__main__":

    if len(sys.argv) == 1:
        # display help
        print("cc <input file> <option = -t2s/-s2t/'none'>")

    if len(sys.argv) > 1:  # at least 2
        data = open(sys.argv[1], "rb").read()
        encoding = detect(data)
        print("Detected input encoding: " + encoding)

    if len(sys.argv) > 2:
        # convert file
        dict_file = "t2s"
        if sys.argv[2] == "-s2t":
            dict_file = "s2t"

        # decode the bytes into unicode string, and convert
        s = convert(data.decode(encoding), construct_dict(dict_file))

        # output result to file
        open("out", "w", encoding="utf8").write(s)
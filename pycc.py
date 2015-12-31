# Chinese characters convert tool
# Traditional <--> Simplified, from any encoding to utf-8.
import sys
import chardet
import os
import glob
from collections import deque


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
		org_f = open(f, "rb")
		org_filename = os.path.basename(org_f.name)
		org_dirname = os.path.dirname(os.path.abspath(org_f.name))
		encoding = detect(org_f.read())
		print(f)
		print("    Suggested encoding:" + encoding)
		s = convert(open(f, "r", encoding=encoding).read(), d)
		open(org_dirname + os.path.sep + "_" + org_filename,
			"w", encoding="utf8").write(s)


def print_help():
	print("Usage: " + os.path.basename(__file__) + " <command> [-g | -glob] <input_files | glob_pattern>")
	print("  command: ")
	print("    -t2s Traditional chinese to Simplified chinese")
	print("    -t2s Simplified chinese to Traditional chinese")
	print("    -i Print suggested encoding only")
	print("  -g, -glob Select files with glob pattern")

if __name__ == "__main__":
	args = deque(sys.argv[1:])

	if len(sys.argv) < 2 or "-h" in args or "-help" in args:
		print_help()
	else:
		try:
			option = args.popleft()[1:]
			if "-g" == args[0] or "-glob" == args[0]:
				args.popleft()
				files = glob.glob(args.popleft())
			else:
				files = args
			cd = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "dict" + os.path.sep
			if option == "i":
				for f in files:
					print("Suggested encoding:" + detect(open(f, "rb").read()))
			elif option == "t2s" or option == "s2t":
				convert_files(construct_dict(cd + option), files)
			else:
				print_help()
		except Exception as e:
			print_help()

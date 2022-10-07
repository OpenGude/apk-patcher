import os
import sys

if len(sys.argv) != 3:
	print(f"USAGE: python3 {sys.argv[0]} input.apk output.apk")
	exit()

input_path, output_path = sys.argv[1:]

os.system(f"apktool d -f -o apk '{input_path}'")

# TODO: patch

os.system(f"apktool b -o '{output_path}' apk")

# TODO: sign it?

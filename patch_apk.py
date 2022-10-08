import os
import sys
from lxml import etree as ET

ORIG_PREFIX = "com.cyberstep"
NEW_PREFIX = "de.opengu"

def patch_manifest():
	manifest = ET.parse("apk/AndroidManifest.xml")

	nsname = "{http://schemas.android.com/apk/res/android}name"

	root = manifest.getroot()
	root.attrib["package"] = root.get("package").replace(ORIG_PREFIX, NEW_PREFIX)

	for elem in list(manifest.iter()):
		name = elem.get(nsname)
		if not name:
			continue
		if "tapjoy" in name.lower() or "firebase" in name.lower() or "onestore" in name.lower():
			print("removing", name)
			elem.getparent().remove(elem)
			continue
		if name.startswith(ORIG_PREFIX):
			print("renaming", name)
			elem.attrib[nsname] = name.replace(ORIG_PREFIX, NEW_PREFIX)

	manifest.write("apk/AndroidManifest.xml", encoding="utf-8", xml_declaration=True, standalone=False)

def patch_res_strings():
	strings =  ET.parse("apk/res/values/strings.xml")
	
	for elem in list(strings.iter()):
		if elem.get("name") == "app_name":
			elem.text = "OpenGude"

	strings.write("apk/res/values/strings.xml", encoding="utf-8", xml_declaration=True)

if len(sys.argv) != 3:
	print(f"USAGE: python3 {sys.argv[0]} input.apk output.apk")
	exit()

input_path, output_path = sys.argv[1:]

os.system(f"apktool d -f -o apk '{input_path}'")

patch_manifest()
patch_res_strings()

os.system(f"apktool b -o '{output_path}' apk")

# TODO: sign the apk?

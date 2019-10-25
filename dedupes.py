import os
import glob
import hashlib

hashes = set()

for filename in sorted(glob.glob("data/*.html")):
    with open(filename) as f:
        md5_value = hashlib.md5(f.read().encode("utf-8")).hexdigest()
        if md5_value in hashes:
            print(f"Deleting {filename}")
            os.remove(filename)
        hashes.add(md5_value)

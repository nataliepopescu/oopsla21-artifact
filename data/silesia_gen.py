import brotli

import random
import string

with open('./silesia.tar', 'rb') as f:
    decoded = f.read()

print("Generating silesia-5...")
with open('silesia-5.brotli', 'wb') as f:
    compressed= brotli.compress(decoded, quality=5)
    f.write(compressed)

print("Generating silesia-11...")
with open('silesia-11.brotli', 'wb') as f:
    compressed= brotli.compress(decoded, quality=11)
    f.write(compressed)

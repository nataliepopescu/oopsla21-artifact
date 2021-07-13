import sys
with open("cal.out", "r") as fd:
    lines = fd.readlines()

startLine = 0
for idx, line in enumerate(lines):
    if "Start of get_unchecked stats" in line:
        startLine = idx + 1

lines = lines[startLine:]
print(sys.argv[1])
for idx, line in enumerate(lines):
    line = line.replace(sys.argv[1], '')
    lines[idx] = line

with open("cal.out", "w") as fd:
    fd.writelines(lines)

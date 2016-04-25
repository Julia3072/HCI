fileOutput = "output.csv"

out = ""

with open('pulse.csv') as openfileobject:
    for line in openfileobject:
        l = str(line)
        if not (l.__contains__("Q") or l.__contains__("B")):
            out += l

print(out)
with open("pulse_parsed.csv", "w") as text_file:
    text_file.write(out)
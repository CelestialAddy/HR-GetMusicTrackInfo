### DumpStreamEventCallsFromXML.py
### Read, output all RMS->XML "StreamEvent" targets by level.
### DEC-2024/CelestialAddy

Lines = []

for N in range(1, 8):
    Get = open("C:/Fake/Not_real/l@_music.xml".replace("@", str(N)), "r")
    XML = Get.read().split("\n")
    Get.close()
    Lines.append("L\t" + str(N) + "\n")
    for Line in XML:
        if (Line.find("<Region") > -1) and (len(Line.split("\"")) > 1):
            Region = Line.split("\"")[1]
            pass
        if (Line.find("<StreamEvent") > -1) and (len(Line.split("\"")) > 1):
            Lines.append(Region + "\t" + Line.split("\"")[1] + "\n")
            pass
        continue
    continue

TextOut = ""
for Line in Lines:
    TextOut = TextOut + Line
    continue
TextFile = open("IO/StreamEventCalls.txt", "w")
TextFile.write(TextOut)
TextFile.close()
input("DumpStreamEventCallsFromXML.py: Done!\n")

### End of file.

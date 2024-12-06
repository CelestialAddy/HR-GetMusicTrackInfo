### DumpRSDFileCallsFromXML.py
### Read, output all RMS->XML "RSDFile" targets by level.
### DEC-2024/CelestialAddy

Lines = []

for N in range(1, 8):
    Get = open("C:/Fake/Not_real/l@_music.xml".replace("@", str(N)), "r") # SWAP IN PATH TO DIR OF RMS->XML FILES.
    XML = Get.read().split("\n")
    Get.close()
    Lines.append("L\t" + str(N) + "\n")
    for Line in XML:
        if (Line.find("<RSDFile") > -1) and (len(Line.split("\"")) > 1):
            Lines.append(Line.split("\"")[1].lower() + "\n")
            pass
        continue
    continue

TextOut = ""
for Line in Lines:
    TextOut = TextOut + Line
    continue
TextFile = open("IO/RSDFileCalls.txt", "w")
TextFile.write(TextOut)
TextFile.close()
input("DumpRSDFileCallsFromXML.py: Done!\n")

### End of file.

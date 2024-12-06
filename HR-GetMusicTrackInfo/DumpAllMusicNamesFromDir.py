### DumpAllMusicNamesFromDir.py
### Get all music ".rsd" names from extracted RCF contents directory.
### DEC-2024/CelestialAddy

import os

Music = []
Paths = [
        "C:/Fake/Not_real/tshr", # ABSOLUTE PATH TO GAME INSTALL HERE.
        "/apu",
        "/bart",
        "/generic",
        "/halloween",
        "/homer",
        "/lisa",
        "/marge",
        "/minigame",
        ]

for Path in Paths:
    if Path == Paths[0]:
        Path = Path + "/"
        SubPath = ""
        pass
    else:
        Path = Paths[0] + Path + "/"
        SubPath = Path.split("/")[len(Path.split("/")) - 2] + "\\"
        pass
    for Item in os.listdir(Path):
        if "/" + Item in Paths:
            continue
        else:
            Music.append(SubPath + Item.split(".")[0])
            pass
        continue

List = ""

for Track in Music:
    List = List + Track + "\n"
    continue

TextFile = open("IO/MusicTracks.txt", "w")
TextFile.write(List)
TextFile.close()
input("DumpAllMusicNamesFromDir.py: Done!\n")

### End of file.

### ConvertTXTToMD.py
### Convert the pre-tool-made all music TXT into a MD document with basic formatting.
### DEC-2024/CelestialAddy

Get = open("IO/_MusicSummaryAll.txt", "r")
TXT = Get.read().split("\n")
Get.close()

Out = [
    "# MusicTrackUsage",
    "This document has been generated through multi-stage music RMS (as XML) script parsings.",
    "- \"IS INITIALISED\" = Track was called via `RSDFile`.",
    "- \"USES ALIAS\" = Track was called (as its `RSDFile`) and given a name via `Stream`.",
    "   - Possibly more than once, if the aliases differ.",
    "   - If multiple share the same alias, that means the exact `Stream` call was duplicated.",
    "- \"IN REGION\" = Track was called (as a `Stream`) via `StreamEvent` in a `Region`.",
    "   - Whether or not this region is actually attached to anything or ever called varies.",
    "- \"ABOVE REGION OVERRULED AS UNUSED\" = This `Region` is never typically called in vanilla.",
    ]

for Ln in TXT:
    Ln = Ln.replace("\"", "`")
    Ln = Ln.replace(" : ", "")
    for L in range(1, 8):
        if Ln.find("L" + str(L)) != -1: Ln = Ln.replace("L" + str(L), "**Level " + str(L) + ":** ")
        continue
    if Ln.count("\t") == 0:
        Ln = "## " + Ln
        pass
    elif Ln.count("\t") == 1:
        Ln = Ln.replace("\t", "- ")
        pass
    elif Ln.count("\t") == 2:
        Ln = Ln.replace("\t\t", "\t- ")
        pass
    else:
        pass
    if len(Ln) == 0:
        Ln = "  "
        pass
    Out.append(Ln)
    continue
Out.append("  \n---")

MDT = ""
for Ln in Out:
    MDT = MDT + Ln + "\n"
    continue
MDF = open("IO/_MusicSummaryAll.md", "w")
MDF.write(MDT)
MDF.close()
input("ConvertTXTToMD.py: Done!\n")

### End of file.

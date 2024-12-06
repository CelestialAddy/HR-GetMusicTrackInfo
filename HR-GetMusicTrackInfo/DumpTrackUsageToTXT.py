### DumpTrackUsageToTXT.py
### Read the output of other scripts and output inferred track usage to TXT indent-heavy lists.
### DEC-2024/CelestialAddy

# Dump stuff we need to use.
Get = open("IO/MusicTracks.txt", "r")
MUS = Get.read().split("\n")
MUS.sort() # Little fix so alphabetical order is used...
Get.close()
Get = open("IO/RSDFileCalls.txt", "r")
RSD = Get.read().split("\n")
Get.close()
Get = open("IO/StreamCalls.txt", "r")
STM = Get.read().split("\n")
Get.close()
Get = open("IO/StreamEventCalls.txt", "r")
EVE = Get.read().split("\n")
Get.close()
Get = open("IO/UnusedRegionBlacklist.txt", "r")
URE = Get.read().split("\n")
Get.close()
Get = open("IO/UnusedTrackBlacklist.txt", "r")
UTR = Get.read().split("\n")
Get.close()

# Work out "we claim/overrule/note for end of TXT" unused regions/tracks lists.
UnuReg = []
for Reg in URE:
    if len(Reg.split("#")[0]) > 0:
        try:
            Reg = Reg.split("#")[0]
            Reg = Reg.split("\t")
            if Reg[1] == str(0):
                for LvlCode in range(1, 8):
                    UnuReg.append(Reg[0] + ":" + str(LvlCode))
                    continue
                pass
            else:
                UnuReg.append(Reg[0] + ":" + Reg[1].replace("\n", ""))
                pass
            pass
        except:
            continue
    continue
UnuTra = []
for Tra in UTR:
    if len(Tra.split("#")[0]) > 0:
        UnuTra.append(Tra.split("#")[0])
        pass
    continue

# Generate the big table, populate with each track name as a list of possible uses to fill later.
BIG = {}
for Lvl in range(1, 8):
    for Tra in MUS:
        if len(Tra) == 0:
            continue
        BIG.update({str(Tra) : []})
        if Tra in UnuTra:
            BIG[Tra].append("\t(ABOVE TRACK OVERRULED AS GLOBALLY UNUSED.)")
        continue
    continue

# Check/append: level, called at all, aliases: calls to.
for Lvl in range(1, 8): # Level...
    Valid = False
    for Rsd in RSD: # Called at all/not called...
        if len(Rsd) == 0:
            continue
        if (Valid == True) and (Rsd.find("L\t") > -1):
            Valid = False
            continue
        if Rsd.replace("\t", "") == "L" + str(Lvl):
            Valid = True
            continue
        if Valid == True:
            if Rsd in BIG.keys():
                BIG[Rsd].append("\tL" + str(Lvl) + " : IS INITIALISED.")
                pass
            else:
                BIG[Rsd].append("\tL" + str(Lvl) + " : IS NOT INITIALISED.")
                pass
            pass
        continue
    Valid = False
    for Stm in STM: # Aliases...
        if len(Stm) == 0:
            continue
        if (Valid == True) and (Stm.find("L\t") > -1):
            Valid = False
            continue
        if Stm.replace("\t", "") == "L" + str(Lvl):
            Valid = True
            continue
        if Valid == True:
            Track = Stm.split("\t")[0]
            Alias = Stm.split("\t")[1]
            if Track in BIG.keys():
                BIG[Track].append("\tL" + str(Lvl) + " : USES ALIAS \"" + str(Alias) + "\".")
                pass
            Valid2 = False
            for Eve in EVE: # Alias calls...
                if len(Eve) == 0:
                    continue
                if (Valid2 == True) and (Eve.find("L\t") > -1):
                    Valid2 = False
                    continue
                if Eve.replace("\t", "") == "L" + str(Lvl):
                    Valid2 = True
                    continue
                if Valid2 == True:
                    Regon = Eve.split("\t")[0]
                    ALias = Eve.split("\t")[1]
                    if (Track in BIG.keys()) and (Alias == ALias):
                        BIG[Track].append("\t\tL" + str(Lvl) + " : " + "IN REGION : \"" + str(Regon) + "\".")
                        if str(Regon + ":" + str(Lvl)) in UnuReg:
                            BIG[Track].append("\t\t(L" + str(Lvl) + " : ABOVE REGION OVERRULED AS UNUSED.)")
                        pass
                    pass
                continue
            pass
        continue
    continue

# Generate entirely unused track list.
AllUnused = []
AllUnusedNamesOnly = []
for Track in list(BIG.keys()):
    Unused = False
    Sum = ""
    for Item in BIG[Track]:
        Sum = Sum + Item.replace("\t", "")
        continue
    if (Sum.find("IN REGION : ") == -1):
        # (a) Is it never called within a region?
        Unused = True
        pass
    if (Sum.count("REGION OVERRULE") == Sum.count("IN REGION :")):
        # (b) Are all regions it is called in marked as unused?
        Unused = True
        pass
    if (Sum.find("TRACK OVERRULE") != -1):
        # (c) Is the track as a whole marked as unused?
        Unused = True
        pass
    if Unused == True:
        CurUnused = Track
        for Item in BIG[Track]:
            CurUnused = CurUnused + "\n\t"
            if Item.find("IN REGION :") != -1: CurUnused = CurUnused + "\t"
            if Item.find("REGION OVERRULE") != -1: CurUnused = CurUnused + "\t"
            CurUnused = CurUnused + Item.replace("\t", "") + ""
        pass
        AllUnused.append(CurUnused)
        AllUnusedNamesOnly.append(Track)
    continue

# Generate in-level(s) unused track list
LvlUnused = []
LvlUnusedNamesOnly = []
for Track in list(BIG.keys()):
    Unused = False
    Sum = ""
    for Item in BIG[Track]:
        Sum = Sum + Item.replace("\t", "")
        continue
    for LvlCode in range(1, 8):
        if (Sum.find("L" + str(LvlCode) + " : IS INIT") != -1) and (Sum.find("L" + str(LvlCode) + " : IN REG") == -1) and (Track not in AllUnusedNamesOnly):
            # (a) Is the track (a1) initialised (and possibly aliased) but never used in a region, and (a2) is the track not marked as globally unused?
            Unused = True
            pass
        elif (Track not in AllUnusedNamesOnly) and (Sum.count("L" + str(LvlCode) + " : IN REG") == Sum.count("(L" + str(LvlCode) + " : ABOVE REGION")) and (Sum.find("L" + str(LvlCode) + " : IS INIT") != -1):
            # (b) Is the track (b1) not marked as globally unused, and (b2) are all in-region calls unused/unreachable, and (b3) is the track even in the level at all?
            Unused = True
            pass
        if Track in LvlUnusedNamesOnly:
            Unused = False
            pass
        if Unused == True:
            CurUnused = Track
            for Item in BIG[Track]:
                CurUnused = CurUnused + "\n\t" + Item.replace("\t", "")
                continue
            pass
            LvlUnused.append(CurUnused)
            LvlUnusedNamesOnly.append(Track)
        continue
    continue

# Write out final TXTs.
Out = open("IO/_MusicSummaryAll.txt", "w")
for Track in list(BIG.keys()):
    Out.write(Track + "\n")
    for Item in BIG[Track]:
        Out.write(Item + "\n")
        continue
    continue
Out.close()
Out = open("IO/_MusicSummaryGlobalUnused.txt", "w")
for Item in AllUnused:
    Out.write(Item + "\n")
    continue
Out.close()
Out = open("IO/_MusicSummaryLocalUnused.txt", "w")
for Item in LvlUnused:
    Out.write(Item + "\n")
    continue
Out.close()
input("DumpTrackUsageToTXT.py: Done!\n")

### End of file.

### DumpTrackUsageToCSV.py
### Read the output of other scripts and output inferred track usage to CSV table.
### DEC-2024/CelestialAddy

Get = open("IO/MusicTracks.txt", "r")
Tracks = Get.read().split("\n")
Get.close()

Get = open("IO/RSDFileCalls.txt", "r")
Inits = Get.read().split("\n")
Get.close()
RSDFileCalls = {"L1" : [], "L2" : [], "L3" : [], "L4" : [], "L5" : [], "L6" : [], "L7" : []}
for Init in Inits:
    if len(Init) == 0:
        continue
    if Init.replace("\t", "") in list(RSDFileCalls.keys()):
        LKey = Init.replace("\t", "")
    else:
        RSDFileCalls[LKey].append(Init)
    continue

Get = open("IO/StreamCalls.txt", "r")
Streams = Get.read().split("\n")
Get.close()
Aliases = {"L1" : [], "L2" : [], "L3" : [], "L4" : [], "L5" : [], "L6" : [], "L7" : []}
for Stream in Streams:
    if len(Stream) == 0:
        continue
    if Stream.replace("\t", "") in list(Aliases.keys()):
        LKey = Stream.replace("\t", "")
    else:
        Aliases[LKey].append(Stream.replace("\t", ":"))
    continue
LvlSpecDupes = {"L1" : {}, "L2" : {}, "L3" : {}, "L4" : {}, "L5" : {}, "L6" : {}, "L7" : {}}
for N in range(1, 8):
    TmpTbl = Aliases["L"+str(N)].copy()
    for Itm in TmpTbl:
        TmpTbl[TmpTbl.index(Itm)] = Itm.split(":")[1]
        continue
    for Itm in TmpTbl:
        LvlSpecDupes["L"+str(N)][str(Itm)] = TmpTbl.count(Itm)
        continue
    continue

Get = open("IO/StreamEventCalls.txt", "r")
Events = Get.read().split("\n")
Get.close()
StreamEventCalls = {"L1" : [], "L2" : [], "L3" : [], "L4" : [], "L5" : [], "L6" : [], "L7" : []}
for Event in Events:
    if len(Event) == 0:
        continue
    if Event.replace("\t", "") in list(StreamEventCalls.keys()):
        LKey = Event.replace("\t", "")
    else:
        StreamEventCalls[LKey].append(Event.replace("\t", ":"))
    continue

Get = open("IO/UnusedRegionBlacklist.txt", "r")
BList1 = Get.read().split("\n")
Get.close()
UnusedRegions = []
for Track in BList1:
    try:
        Track = Track.split("#")[0]
        Track = Track.split("\t")
        if Track[1] == str(0):
            for N in range(1, 8):
                UnusedRegions.append(Track[0] + ":" + str(N))
                continue
            pass
        else:
            UnusedRegions.append(Track[0] + ":" + Track[1])
            pass
    except:
        continue
    continue

Get = open("IO/UnusedTrackBlacklist.txt", "r")
BList2 = Get.read().split("\n")
Get.close()
UnusedTracks = []
for Track in BList2:
    Track = Track.split("#")[0]
    if len(Track) == 0:
        continue
    else:
        UnusedTracks.append(Track)
    continue

CSVTBL = ["Track,L1 I,L1 A,L2 I,L2 A,L3 I,L3 A,L4 I,L4 A,L5 I,L5 A,L6 I,L6 A,L7 I,L7 A"]

BIG = {}

for Track in Tracks: # Add levels.
    BIG[Track] = {"L1" : {}, "L2" : {}, "L3" : {}, "L4" : {}, "L5" : {}, "L6" : {}, "L7" : {}}
    continue

for Track in list(BIG.keys()): # Add datas.
    for N in range(1, 8):
        BIG[Track]["L" + str(N)]["I"] = 0    # Initialisation count.
        BIG[Track]["L" + str(N)]["A"] = {}   # Dictionary of aliases ([alias]=[region1, ...]).
        continue
    continue

for Track in list(BIG.keys()): # Add inits.
    for N in range(1, 8):
        for Call in RSDFileCalls["L" + str(N)]:
            if Track == Call:
                BIG[Track]["L" + str(N)]["I"] = BIG[Track]["L" + str(N)]["I"] + 1
            continue
        continue
    continue

for Track in list(BIG.keys()): # Add alis.
    for N in range(1, 8):
        for Alias in Aliases["L" + str(N)]:
            xTrack = Alias.split(":")[0]
            xAlias = Alias.split(":")[1]
            if Track == xTrack:
                # This operation is somewhat lossy in that it cannot preserve/note exact DUPE Stream/alias calls...
                # ... not that this effectively matters or for the CSV...
                # Nevermind, hacked in, see later code...
                BIG[Track]["L" + str(N)]["A"][str(xAlias)] = []
            continue
        continue
    continue

for Track in list(BIG.keys()): # Add aliregcalls.
    for N in range(1, 8):
        for Alias in BIG[Track]["L" + str(N)]["A"]:
            for SEC in StreamEventCalls["L" + str(N)]:
                xReg = SEC.split(":")[0]
                xAli = SEC.split(":")[1]
                if Alias == xAli:
                    BIG[Track]["L" + str(N)]["A"][str(xAli)].append(xReg)
                continue
            continue
        continue
    continue

for Track in list(BIG.keys()): # Make CSV lines
    if len(Track) == 0:
        continue
    X = "@TR,@1I,@1A,@2I,@2A,@3I,@3A,@4I,@4A,@5I,@5A,@6I,@6A,@7I,@7A"
    if Track in UnusedTracks:
        X = X.replace("@TR", str(Track) + "*")
    else:
        X = X.replace("@TR", str(Track))
    for N in range(1, 8): # Inits.
        #input(RSDFileCalls)
        #X = X.replace("@"+str(N)+"I", str(BIG[Track]["L" + str(N)]["I"]))
        X = X.replace("@"+str(N)+"I", str(RSDFileCalls["L"+str(N)].count(Track))) # Hack mess 2.0 to include/verify dupe RSDFile calls... because that MATTERS...
        continue
    for N in range(1, 8): #Alis+regs.
        WIPSTR = ""
        #WIPSTR = WIPSTR + "(" + str(len(list(BIG[Track]["L" + str(N)]["A"].keys()))) + ")"
        WIPSTR = WIPSTR + "(" + "@@" + ")"
        #if len(list(BIG[Track]["L" + str(N)]["A"].keys())) > 1:
            #input(list(BIG[Track]["L" + str(N)]["A"].keys()))
        InitialAliasCount = len(list(BIG[Track]["L" + str(N)]["A"].keys()))
        for Alias in list(BIG[Track]["L" + str(N)]["A"].keys()):
            InitialAliasCount = InitialAliasCount + (LvlSpecDupes["L"+str(N)][str(Alias)] - 1) # account for dupes AND precount by keys
            WIPSTR = WIPSTR + "(" + Alias + ": "
            for AliasInstance in BIG[Track]["L" + str(N)]["A"][Alias]:
                WIPSTR = WIPSTR + AliasInstance
                if AliasInstance + ":" + str(N) in UnusedRegions:
                    WIPSTR = WIPSTR + "*"
                if BIG[Track]["L" + str(N)]["A"][Alias].index(AliasInstance) != len(BIG[Track]["L" + str(N)]["A"][Alias]) - 1:
                    WIPSTR = WIPSTR + "/"
                else:
                    WIPSTR = WIPSTR + ")"
                continue
            if len(BIG[Track]["L" + str(N)]["A"][Alias]) == 0:
                WIPSTR = WIPSTR + "N/A)"
            #WIPSTR = WIPSTR.replace("@@", str(InitialAliasCount))
            #WIPSTR = WIPSTR.replace("@@", str(0)) # catch non-alias in level
            continue
        WIPSTR = WIPSTR.replace("@@", str(InitialAliasCount))
        WIPSTR = WIPSTR.replace("@@", str(0)) # catch non-alias in level
            #WIPSTR = WIPSTR + ")"
        X = X.replace("@"+str(N)+"A", WIPSTR)
        continue
    Bads = ["@1I", "@1A", "@2I", "@2A", "@3I", "@3A", "@4I", "@4A", "@5I", "@5A", "@6I", "@6A", "@7I", "@7A"]
    for Bad in Bads:
        X = X.replace(Bad, "N/A")
        continue
    CSVTBL.append(X)
    continue

# Hack mess to mark whole tracks as actually unused or not.
for Track in Tracks:
    Unused = True
    XRegions = []
    if len(Track) == 0:
        continue # this apparently needs to be a thing?? what????
    for N in range(1, 8):
        for R1 in list(BIG[Track]["L" + str(N)]["A"].keys()):
            for R2 in BIG[Track]["L" + str(N)]["A"][R1]:
                if str(R2 + ":" + str(N)) not in UnusedRegions:
                    Unused = False
                continue
            continue
        continue
    if Unused == True:
        #input("def unused: " + Track)
        for Line in CSVTBL:
            if (Line.find(Track) != -1) and (Line.find(Track + "*") == -1): CSVTBL[CSVTBL.index(Line)] = Line.replace(Track, Track + "*")
            continue
    continue

Out = open("IO/_MusicSummaryTable.csv", "w")
for Line in CSVTBL:
    Out.write(Line + "\n")
Out.close()
input("DumpTrackUsageToCSV.py: Done!\n")

### End of file.

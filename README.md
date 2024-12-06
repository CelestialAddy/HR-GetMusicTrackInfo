# HR-GetMusicTrackInfo
A set of (crude, non-user-facing, non-XML-format-compliant) Python scripts for dumping music track existence/usage information from the game data of *The Simpsons: Hit & Run*.
Used to collect/generate displays of information for some documentation in [**SHR-InfoDumps**](https://github.com/CelestialAddy/SHR-InfoDumps/tree/main). Provided in case of usefulness and/or for method verification. Reuse/edits: go for it.

## Scripts, Inputs and Outputs
The ".py" Python scripts are in "/HR-GetMusicTrackInfo"; "/HR-GetMusicTrackInfo/IO" holds input/output files.

### DumpAllMusicNamesFromDir
- This script gets a list of music tracks in the game, from a directory containing an extracted "/sound/music" game directory.
- You must edit the script to set the root search path to your own copy of this extracted directory.
- Outputs as newline-separated "MusicTracks.txt".

### DumpRSDFileCallsFromXML
- This script gets a list of every "RSDFile"/track-initialisation call in each Level (1-7)'s music script from a directory containing them.
- You must edit the script to set the search path to your own copy of this directory.
- Outputs as newline-separated "RSDFileCalls.txt".
	- An occurance of "L", and then an indent, and then "#" (where "#" is a number from 1-7) means "henceforth, calls come from this Level number".

### DumpStreamCallsFromXML
- This script gets a list of every "Stream"/track-alias call in each Level (1-7)'s music script from a directory containing them.
- You must edit the script to set the search path to your own copy of this directory.
- Outputs as newline-separated "StreamCalls.txt".
	- Each line represents a call: a track filename, and then an indent, and then the alias assigned.
	- An occurance of "L", and then an indent, and then "#" (where "#" is a number from 1-7) means "henceforth, calls come from this Level number"

### DumpStreamEventCallsFromXML
- This script gets a list of every "StreamEvent"/track-alias-assign-to-region call in each Level (1-7)'s music script from a directory containing them.
- You must edit the script to set the search path to your own copy of this directory.
- Outputs as newline-separated "StreamEventCalls.txt".
	- Each line represents a call: the alias called, and then an indent, and then the region it was assigned within.
	- An occurance of "L", and then an indent, and then "#" (where "#" is a number from 1-7) means "henceforth, calls come from this Level number"

### DumpTrackUsageToTXT
- This script uses the output of all the prior scripts listed, and the blacklists outlined later, to create a summary list of every music track and its usage by Level.
- Outputs multple lists:
	- "_MusicSummaryAll.txt": Every music track and usage by level; notes unused tracks/regions.
	- "_MusicSummaryGlobalUnused.txt": Every music track that has been inferred to be unused throughout the whole game; notes calls made in reference to each per Level.
	- "_MusicSummaryLocalUnused.txt": Every music track that has been inferred to have at least one "loose end" call; notes calls made in reference to each per Level.
- Outputs use consistent layout and wording, should be fairly simple to machine-parse.
- A track is inferred to be/considered unused if any of these conditions are met:
	- It is in the track blacklist.
	- It is never initialised at all.
	- It is never assigned to a region through an alias at all.
	- If the only assignments it has are for regions marked as unused/unreachable on the region blacklist.

### ConvertTXTToMD
- This script outputs and edited copy ("_MusicSummaryAll.md") of the output of the prior listed script, embellished with basic Markdown document formatting.

### DumpTrackUsageToCSV
- This script uses the output of all the prior scripts listed (except "ConvertTXTToMD.py"), and the blacklists outlined later, to create a summary table (with header row) of every music track and its usage by Level.
- Outputs as newline- (row) and comma- (column) separated "_MusicSummaryTable.csv"; inferred unused tracks/regions marked with asterisk ("*").
- Allows the information to be shown in condensed form; possibly more difficult to machine-parse some details.
- A track is inferred to be/considered unused if any of these conditions are met:
	- It is in the track blacklist.
	- It is never initialised at all.
	- It is never assigned to a region through an alias at all.
	- If the only assignments it has are for regions marked as unused/unreachable on the region blacklist.

## Blacklists
There are two blacklists; they allow indicating to the TXT/CSV output scripts which tracks/regions are unused/unreachable, so that this information can be further inferred and marked in outputs.
Blacklists are plain-text ".txt" files, newline-separated, and ignore content on a single line after a "#" is found, if present.

### UnusedTrackBlacklist
Lists tracks that are entirely unused, period. Quite crude/definite, and not used for the example/InfoDumps outputs. Made before the region blacklist was an idea and maintained only for "just-in-case"/convenience purposes.
Non-TSH&R-relevant example:
```
# UnusedTrackBlacklist.txt

missionTheme1
missionTheme2
missionTheme3
\character\wander146

# END.
```

### UnusedRegionBlacklist
Lists regions that are unused/reachable, as far as is currently known. Line format should be the region name (case-sensitive), and then an indent, and then a number indicating the Level the region is used/unreachable in (one per line; it is valid to re-specify the same region multiple times with different Level numbers, or to use 0 to mark the region as unused/unreachable in every Level).
```
# UnusedRegionBlacklist.txt

GameStart_region	0
Mission112_region	1
Mission742_region	5
Mission742_region	8

# END.
```

## Notes
- All track/path names for music tracks handled/output are relative to the root; "tuba_001.rsd" is always named "homer\tuba_001.rsd".
- All track/path names for music tracks are handled/output as lowercase.
- Duplicate initialisations/aliases are tracked, handled, and preserved in outputs.
	- ".txt"/".md": Text appears repeatedly for each duplicate action.
	- ".csv": All "I/A" cells begin with a number counting that action for each track in each Level; for aliases, if the number is higher than the number of bracketed aliases shown, there is a/are duplicates.
- All ".xml" inputs are parsed using custom logic and not an XML-compliant parser. The custom parser should work for any RMS->XML output from Lucas' RadScript Music Builder, but may not entirely or at all work for all valid RMS->XML *inputs* to that tool, for example if they make use of the "Include" tag or place multiple relevant tags on the same line.
- All outputs contain a blank line at the very end.
- The input/output files specified above are already present in this upload, for reference/replacement if desired.
- The only requirement outside of the files provides/specified above is access to the "os" standard library module in Python, specifically only for the "DumpAllMusicNamesFromDir.py" script.

---

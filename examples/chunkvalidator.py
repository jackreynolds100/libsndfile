import struct
from operator import itemgetter, attrgetter
import sys

if len(sys.argv) > 1:
    filePath = sys.argv[1]
else:
    print "ERROR: Must provide path to file as an argument!"
    exit(1)

# filePath = "C:\\Users\\matthewf\\Desktop\\elbow.wav"
# filePath = "C:\\Users\\matthewf\\Desktop\\flower_duet_bwf.wav"
# filePath = "C:\\Users\\matthewf\\Downloads\\BW64_4gb_sine.wav"

# varType has the following options:
# - ckSize: This is technically an int, but checks for the special 0xFFFF value which indicates size is denoted by a DS64 table entry
# - string: As strandard, but can be used for any data really (e.g, waveData)
# - int: Standard integer
# - chunks: nested chunks definied in the innerChunks property of that chunk

innerChunks = {
    "ds64": {
        "structure": [
            {"varName": "chunkId", "varSize": 4, "varType": "string", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "chunkSize", "varSize": 4, "varType": "ckSize", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "bw64Size", "varSize": 8, "varType": "int", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "dataSize", "varSize": 8, "varType": "int", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "dummy", "varSize": 8, "varType": "int", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "tableLength", "varSize": 4, "varType": "int", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "table", "varSizeMultiple": 12, "varSizeMin": 0, "varSizeMax": None, "varType": "chunks", "content": None, "value": None, "contentLength": None, "mandatory": False}
            ],
        "innerChunks": {
            "table": {
                "structure": [
                    {"varName": "chunkId", "varSize": 4, "varType": "string"},
                    {"varName": "chunkSize", "varSize": 8, "varType": "int"}
                    ]
                }
            },
        "tagMatchPositions": [],
        "chunkHeaderSize": 8,
        "chunkStart": None,
        "chunkOwnLength": None,
        "chunkDs64Length": None,
        "chunkEnd": None
        },
    "fmt": {
        "structure": [
            {"varName": "chunkId", "varSize": 4, "varType": "string", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "chunkSize", "varSize": 4, "varType": "ckSize", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "formatTag", "varSize": 2, "varType": "int", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "channelCount", "varSize": 2, "varType": "int", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "sampleRate", "varSize": 4, "varType": "int", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "bytesPerSecond", "varSize": 4, "varType": "int", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "blockAlignment", "varSize": 2, "varType": "int", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "bitsPerSample", "varSize": 2, "varType": "int", "content": None, "value": None, "contentLength": None, "mandatory": False}, # 1991 RIFF MCI spec
            {"varName": "cbSize", "varSize": 2, "varType": "int", "content": None, "value": None, "contentLength": None, "mandatory": False},
            {"varName": "extraData", "varSizeMultiple": 1, "varSizeMin": 0, "varSizeMax": None, "varType": "string", "content": False, "value": False, "contentLength": None, "mandatory": False} # False denotes "do not store" (because variable length, this could be accidently HUGE! - we don't validate actual content anyway)
            ],
        "innerChunks": {
            },
        "tagMatchPositions": [],
        "chunkHeaderSize": 8,
        "chunkStart": None,
        "chunkOwnLength": None,
        "chunkDs64Length": None,
        "chunkEnd": None
        },
    "chna": {
        "structure": [
            {"varName": "chunkId", "varSize": 4, "varType": "string", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "chunkSize", "varSize": 4, "varType": "ckSize", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "numTracks", "varSize": 2, "varType": "int", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "numUIDs", "varSize": 2, "varType": "int", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "ID", "varSizeMultiple": 40, "varSizeMin": 0, "varSizeMax": None, "varType": "chunks", "content": None, "value": None, "contentLength": None, "mandatory": True}
            ],
        "innerChunks": {
            "ID": {
                "structure": [
                    {"varName": "trackIndex", "varSize": 2, "varType": "int"},
                    {"varName": "UID", "varSize": 12, "varType": "string"},
                    {"varName": "trackRef", "varSize": 14, "varType": "string"},
                    {"varName": "packRef", "varSize": 11, "varType": "string"},
                    {"varName": "pad", "varSize": 1, "varType": "string"}
                    ]
                }
            },
        "tagMatchPositions": [],
        "chunkHeaderSize": 8,
        "chunkStart": None,
        "chunkOwnLength": None,
        "chunkDs64Length": None,
        "chunkEnd": None
        },
    "axml": {
        "structure": [
            {"varName": "chunkId", "varSize": 4, "varType": "string", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "chunkSize", "varSize": 4, "varType": "ckSize", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "xmlData", "varSizeMultiple": 1, "varSizeMin": 0, "varSizeMax": None, "varType": "string", "content": False, "value": False, "contentLength": None, "mandatory": True} # False denotes "do not store" (because variable length, this could be accidently HUGE! - we don't validate actual content anyway)
            ],
        "innerChunks": {
            },
        "tagMatchPositions": [],
        "chunkHeaderSize": 8,
        "chunkStart": None,
        "chunkOwnLength": None,
        "chunkDs64Length": None,
        "chunkEnd": None
        },
    "data": {
        "structure": [
            {"varName": "chunkId", "varSize": 4, "varType": "string", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "chunkSize", "varSize": 4, "varType": "ckSize", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "waveData", "varSizeMultiple": 1, "varSizeMin": 0, "varSizeMax": None, "varType": "string", "content": False, "value": False, "contentLength": None, "mandatory": True} # False denotes "do not store" - we don't validate actual content anyway # TODO: varSizeMultiple should really be channelCount*bitsPerSample/8
            ],
        "innerChunks": {
            },
        "tagMatchPositions": [],
        "chunkHeaderSize": 8,
        "chunkStart": None,
        "chunkOwnLength": None,
        "chunkDs64Length": None,
        "chunkEnd": None
        },
    "JUNK": {
        "structure": [
            {"varName": "chunkId", "varSize": 4, "varType": "string", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "chunkSize", "varSize": 4, "varType": "ckSize", "content": None, "value": None, "contentLength": None, "mandatory": True},
            {"varName": "chunkData", "varSizeMultiple": 1, "varSizeMin": 28, "varSizeMax": None, "varType": "string", "content": False, "value": False, "contentLength": None, "mandatory": True} # False denotes "do not store" - we don't validate actual content anyway # TODO: varSizeMultiple should really be channelCount*bitsPerSample/8
            ],
        "innerChunks": {
            },
        "tagMatchPositions": [],
        "chunkHeaderSize": 8,
        "chunkStart": None,
        "chunkOwnLength": None,
        "chunkDs64Length": None,
        "chunkEnd": None
        }
    }

outerChunk = {
    "structure": [
        {"varName": "chunkId", "varSize": 4, "varType": "string", "content": None, "value": None, "contentLength": None, "mandatory": True},
        {"varName": "chunkSize", "varSize": 4, "varType": "ckSize", "content": None, "value": None, "contentLength": None, "mandatory": True},
        {"varName": "riffType", "varSize": 4, "varType": "string", "content": None, "value": None, "contentLength": None, "mandatory": True}
        ],
    "innerChunks": innerChunks,
    "chunkHeaderSize": 8,
    "chunkStart": 0,
    "chunkOwnLength": None,
    "chunkDs64Length": None,
    "chunkEnd": None
    }


def getObjFromArray(arr, key, val):
    i = 0
    while i<len(arr):
        obj = arr[i]
        if type(obj) == dict:
            if key in obj and obj[key] == val:
                return obj
        i = i+1
    return None

def _populateChunkDims(chunkObj, fileContent, startPos):
    chunkObj["chunkStart"] = startPos

    # Look for the special ckSize varType...
    posWithinChunk = 0
    chunkIdLen = None # Normally excluded in chunk lengths, so we need to know this to figure out the true end position of the chunk
    chunkSizeLen = None # Normally excluded in chunk lengths, so we need to know this to figure out the true end position of the chunk
    chunkSize = None

    for varObj in chunkObj["structure"]:
        if varObj["varName"] == "chunkId":
            chunkIdLen = varObj["varSize"]
        if varObj["varName"] == "chunkSize" and varObj["varType"] == "ckSize":
            chunkSizeLen = varObj["varSize"]
            chunkSize = fileContent[startPos+posWithinChunk:startPos+posWithinChunk+varObj["varSize"]]
        if "varSize" not in varObj:
            break # No need to continue from here.. this is variable length data which is probably at the end of the chunk
        posWithinChunk = posWithinChunk + varObj["varSize"]

    if chunkObj["chunkHeaderSize"] is None and chunkIdLen is not None and chunkSizeLen is not None:
        chunkObj["chunkHeaderSize"] = chunkIdLen + chunkSizeLen

    if chunkSize is not None and leToInt(chunkSize) <> -1:
        chunkObj["chunkOwnLength"] = leToInt(chunkSize)
        chunkObj["chunkEnd"] = chunkObj["chunkStart"] + chunkObj["chunkHeaderSize"] + chunkObj["chunkOwnLength"]
    elif chunkObj["chunkDs64Length"] is not None:
        chunkObj["chunkEnd"] = chunkObj["chunkStart"] + chunkObj["chunkHeaderSize"] + chunkObj["chunkDs64Length"]


def populateOuterChunkDims(outerChunk, fileContent):
	if outerChunk["chunkStart"] is not None:
		_populateChunkDims(outerChunk, fileContent, outerChunk["chunkStart"])
	else:
		_populateChunkDims(outerChunk, fileContent, 0)


def populateInnerChunksDims(innerChunks, fileContent, searchStartPos=8): # startPos excludes outer chunk header
    # When this is called, all DS64 sizes have already been passed in to the chunkDs64Length properties

    tagMatchesAll = []

    for chunkName in innerChunks:
        pos = fileContent.find(chunkName.ljust(4), searchStartPos)
        while pos >=0:
            innerChunks[chunkName]["tagMatchPositions"].append(pos)
            tagMatchesAll.append({"tag": chunkName, "pos": pos})
            pos = fileContent.find(chunkName.ljust(4), pos+1)

    if len(tagMatchesAll) == 0:
        return # No tags to process

    # Order the tagMatches array
    tagMatchesAll = sorted(tagMatchesAll, key=itemgetter("pos"))

    # Tags can not be processed twice...
    currentPos = tagMatchesAll[0]["pos"]
    doneTags = []

    # Go through them in order
    for tagMatchObj in tagMatchesAll:
        if tagMatchObj["tag"] not in doneTags and tagMatchObj["pos"] >= currentPos:
            _populateChunkDims(innerChunks[tagMatchObj["tag"]], fileContent, tagMatchObj["pos"])
            doneTags.append(tagMatchObj["tag"])
            currentPos = innerChunks[tagMatchObj["tag"]]["chunkEnd"]

    # Now all chunks which are present and not overlapped by another chunk will have a chunkStart
    #  - this ensures the tag names in other chunk contents are not interpretted as the start of other chunks.
    #    however, all found tag positions are in the chunks "tagMatchPositions" property,
    #     so we can indicate possible chunk starts that have been accidently overlapped by another chunk

    # All chunks which are present and not overlapped by another chunk will have a chunkOwnLength (if it wasn't -1)

    # All chunks mentioned in the DS64 table have a chunkDs64Length (this was already populated prior to calling this func)

    # Chunks SHOULD therefore have a chunkEnd, but this may not be the case if the chunks own size parameter was -1 and it also wasn't listed in DS64


def orderChunks(innerChunks):
    chunkOrder = []

    for chunkName in innerChunks:
        thisPos = innerChunks[chunkName]["chunkStart"]
        if thisPos is not None:

            # Insert in to the right place in the ordered list
            inserted = False
            i = 0
            while i < len(chunkOrder):
                thatPos = innerChunks[chunkOrder[i]]["chunkStart"]
                if thisPos < thatPos:
                    inserted = True
                    chunkOrder.insert(i, chunkName)
                    break
                i = i+1
            if not inserted:
                chunkOrder.append(chunkName)

    return chunkOrder

def readChunk(chunkObj, fileContent, maxFilePos=None):
    if maxFilePos is None:
        maxFilePos = len(fileContent)
    if chunkObj["chunkEnd"] is not None and chunkObj["chunkEnd"] < maxFilePos:
        maxFilePos = chunkObj["chunkEnd"]

    filePos = chunkObj["chunkStart"]

    for varObj in chunkObj["structure"]:
        varSize = 0

        if "varSize" in varObj:
            varSize = varObj["varSize"]
        elif "varSizeMultiple" in varObj:
            unmultipleBytes = (maxFilePos-filePos)%varObj["varSizeMultiple"] # Modulo of remaining chunk bytes divided by the multiple they must be in
            varSize = maxFilePos-filePos-unmultipleBytes
        else:
            varSize = maxFilePos-filePos # Just use remainder of chunk

        # Make sure varSize satisfies minimum and maximum if defined
        if "varSizeMin" in varObj and varObj["varSizeMin"] is not None and varSize < varObj["varSizeMin"]:
            varSize = varObj["varSizeMin"]
        if "varSizeMax" in varObj and varObj["varSizeMax"] is not None and varSize > varObj["varSizeMax"]:
            varSize = varObj["varSizeMax"]

        # Make sure this doesn't make us go out of bounds
        if filePos+varSize > maxFilePos:
            #print "BREAK"
            break

        # Put the data in the var

        varObj["contentLength"] = varSize

        if varObj["varType"] == "ckSize":
            if varObj["content"] is not False:
                varObj["content"] = fileContent[filePos:filePos+varSize]
            if varObj["value"] is not False:
                varObj["value"] = -1
                if leToInt(fileContent[filePos:filePos+varSize], True) <> -1:
                    varObj["value"] = leToInt(fileContent[filePos:filePos+varSize])

        elif varObj["varType"] == "int":
            if varObj["content"] is not False:
                varObj["content"] = fileContent[filePos:filePos+varSize]
            if varObj["value"] is not False:
                varObj["value"] = leToInt(fileContent[filePos:filePos+varSize])

        else: #Strings and nested chunk types can just be dumped in as-is.
            if varObj["content"] is not False:
                varObj["content"] = fileContent[filePos:filePos+varSize]
            if varObj["value"] is not False:
                varObj["value"] = fileContent[filePos:filePos+varSize]

        # Seek ahead
        filePos = filePos + varSize

def readChunks(innerChunks, chunkOrder, fileContent):
    i = 0
    while i < len(chunkOrder):
        thisChunk = innerChunks[chunkOrder[i]]
        maxChunkEnd = None  # Default when there is no next chunk
        if i+1 < len(chunkOrder):
            maxChunkEnd = innerChunks[chunkOrder[i+1]]["chunkStart"]
        readChunk(thisChunk, fileContent, maxChunkEnd)
        i = i+1

def updateChunkSizesFromDs64(innerChunks):
    # if "ds64" not in innerChunks or "structure" not in innerChunks["ds64"]:
        # throw("Error: ds64 not in innerChunks or doesn't have structure")
    # if "innerChunks" not in innerChunks["ds64"] or "table" not in innerChunks["ds64"]["innerChunks"] or "structure" not in innerChunks["ds64"]["innerChunks"]["table"]:
        # throw("Error: expected innerChunks prop with table prop with structure prop inside ds64 in innerChunks")

    # Remember what we discovered in the table
    tableEntries = {}

    # DATA and BW64 chunk sizes!!
    bw64SizeObj = getObjFromArray(innerChunks["ds64"]["structure"], "varName", "bw64Size")
    if bw64SizeObj["value"] is not None:
        outerChunk["chunkDs64Length"] = bw64SizeObj["value"]
        outerChunk["chunkEnd"] = outerChunk["chunkStart"] + outerChunk["chunkHeaderSize"] + outerChunk["chunkDs64Length"]
    dataSizeObj = getObjFromArray(innerChunks["ds64"]["structure"], "varName", "dataSize")
    if dataSizeObj["value"] is not None:
        innerChunks["data"]["chunkDs64Length"] = dataSizeObj["value"]


    # Locate the table in DS64
    i = 0
    varObj = None

    while i < len(innerChunks["ds64"]["structure"]):
        varObj = innerChunks["ds64"]["structure"][i]
        if varObj["varName"] == "table" and varObj["varType"] == "chunks":
            break
        i = i+1

    if varObj is None:
        throw("Error: No varName of table with varType of chunks")
    else:

        # varObj["content"] holds the raw table data
        pos = 0
        outOfBounds = (pos < varObj["contentLength"])

        while not outOfBounds:
            ckName = None
            ckSize = None

            for tableVarObj in innerChunks["ds64"]["innerChunks"]["table"]["structure"]:

                if pos+tableVarObj["varSize"] > varObj["contentLength"]:
                    outOfBounds = True
                    break

                tvoValue = varObj["content"][pos:pos+tableVarObj["varSize"]]

                if tableVarObj["varName"] == "chunkId":
                    ckName = tvoValue
                    ckSize = None
                elif tableVarObj["varName"] == "chunkSize":
                    ckSize = tvoValue

                pos = pos+tableVarObj["varSize"]

            if ckName is not None:
                tableEntries[ckName] = ckSize
                if ckSize is not None and ckName in innerChunks:
                    innerChunks[ckName]["chunkDs64Length"] = leToInt(ckSize)

    return bw64SizeObj["content"], dataSizeObj["content"], tableEntries


def o(heading, value, successful=None, outcome_text=None, value_trim=False, heading_length=32, value_length=32):

    if len(heading + ": ") <= heading_length:
        heading = (heading + ": ").ljust(heading_length)
    else:
        heading = heading[:heading_length-5] + "...: "

    if value is None:
        value = "[MISSING]"
    else:
        value = str(value)

    if len(value) <= value_length:
        value = value.ljust(value_length)
    else:
        value = value[:value_length-4] + "... "

    if outcome_text is not None and len(outcome_text) > 0:
        outcome_text = "(" + outcome_text + ")"
    else:
        outcome_text = ""

    if successful is True:
        print heading + value + "Valid!   " + outcome_text
    elif successful is False:
        print heading + value + "INVALID! " + outcome_text
    else:
        print heading + value + "         " + outcome_text


def reportLe(inp, signed=False):
    if inp == None:
        return "[NOT FOUND]"
    return str(leToInt(inp, signed)) + " (0x" + inp.encode("hex").upper() + ")"

def leToInt(inp, signed=False):
    if signed:
        return struct.unpack('>i', inp)[0]
    return int(inp[::-1].encode("hex"), 16)




















content = ""

print "\nLoading file..."
with open(filePath, "rb") as content_file:
    content = content_file.read()
print "File Loaded!\n"

print "Determining outer chunk position and dimensions..."
populateOuterChunkDims(outerChunk, content)

print "Reading outer chunk header..."
readChunk(outerChunk, content)

print "Checking for DS64 chunk..."
ds64Pos = content.find("ds64", outerChunk["chunkHeaderSize"])
ds64Bw64Size = None
ds64DataSize = None
ds64TableEntries = None
if ds64Pos >= 0:
    print "Found DS64 chunk ID. Reading chunk..."
    chunkObj = innerChunks["ds64"]
    _populateChunkDims(chunkObj, content, ds64Pos)
    readChunk(chunkObj, content)
    print "Updating chunk sizes from DS64..."
    ds64Bw64Size, ds64DataSize, ds64TableEntries = updateChunkSizesFromDs64(innerChunks)
else:
    print "   No DS64 chunk ID found"

print "Determining inner chunk positions and dimensions..."
populateInnerChunksDims(innerChunks, content, outerChunk["chunkHeaderSize"])

print "Determining inner chunk order..."
chunkOrder = orderChunks(innerChunks)

print "Reading inner chunks..."
readChunks(innerChunks, chunkOrder, content)
print "Done!"

# Now some validation

print "\nOUTER CHUNK\n"

#   Values from vars in structure

outerChunkIdObj = getObjFromArray(outerChunk["structure"], "varName", "chunkId")
heading = "Chunk chunkId Parameter"
if outerChunkIdObj["value"] == "BW64" or outerChunkIdObj["value"] == "RIFF":
    o(heading, outerChunkIdObj["value"], True)
elif outerChunkIdObj["contentLength"] is None:
    o(heading, outerChunkIdObj["value"], False, "could not read value")
else:
    o(heading, outerChunkIdObj["value"], False, "unexpected ID (this tool supports 'RIFF' and 'BW64')")

outerChunkSizeObj = getObjFromArray(outerChunk["structure"], "varName", "chunkSize")
heading = "Chunk chunkSize Parameter"
if outerChunkSizeObj["contentLength"] is not None:
    if outerChunkIdObj["value"] == "BW64":
        o(heading, reportLe(outerChunkSizeObj["content"], (outerChunkSizeObj["value"] == -1)), (outerChunkSizeObj["value"] == -1), "expecting -1 for BW64")
    else:
        o(heading, reportLe(outerChunkSizeObj["content"], (outerChunkSizeObj["value"] == -1)), (outerChunkSizeObj["value"] <> -1), "only expecting -1 for BW64")
else:
    o(heading, outerChunkSizeObj["value"], False, "could not read value")

riffTypeObj = getObjFromArray(outerChunk["structure"], "varName", "riffType")
heading = "Chunk riffType Parameter"
if riffTypeObj["value"] == "WAVE":
    o(heading, riffTypeObj["value"], True)
elif riffTypeObj["contentLength"] is None:
    o(heading, riffTypeObj["value"], False, "could not read value")
else:
    o(heading, riffTypeObj["value"], False, "expect 'WAVE'")

#   Chunk dimension

if outerChunkIdObj["value"] == "BW64":
    heading = "DS64 Stated Size"
    ds64Bw64SizeObj = getObjFromArray(innerChunks["ds64"]["structure"], "varName", "bw64Size")
    if outerChunk["chunkDs64Length"] is not None:
        lofAndChunkDiff = len(content)-outerChunk["chunkDs64Length"] - outerChunk["chunkHeaderSize"]
        if lofAndChunkDiff == 0:
            o(heading, reportLe(ds64Bw64SizeObj["content"]), True, "DS64 specified size spans entire file")
        else:
            term = "shorter"
            if lofAndChunkDiff > 0:
                term = "longer"
            o(heading, reportLe(ds64Bw64SizeObj["content"]), False, "file is " + str(abs(lofAndChunkDiff)) + " bytes " + term + " than chunk")
    else:
        o(heading, outerChunk["chunkDs64Length"], False, "expecting size to be specified by DS64")
else:
    heading = "Self-Stated Size"
    if outerChunk["chunkOwnLength"] is not None:
        lofAndChunkDiff = len(content)-outerChunk["chunkOwnLength"] - outerChunk["chunkHeaderSize"]
        if lofAndChunkDiff == 0:
            o(heading, reportLe(outerChunkSizeObj["content"], (outerChunkSizeObj["value"] == -1)), True, "size spans entire file")
        else:
            term = "shorter"
            if lofAndChunkDiff > 0:
                term = "longer"
            o(heading, reportLe(outerChunkSizeObj["content"], (outerChunkSizeObj["value"] == -1)), False, "file is " + str(abs(lofAndChunkDiff)) + " bytes " + term + " than chunk")
    else:
        o(heading, outerChunk["chunkOwnLength"], False, "length not specified by outer chunk header")

# Validate presence of inner chunks

print "\nINNER CHUNK PRESENCE\n"

mandatoryInnerChunks = ["fmt", "data"] # Non-BW64
if outerChunkIdObj["value"] == "BW64":
    mandatoryInnerChunks = ["fmt", "data", "ds64"] # Non-BW64
optionalInnerChunks = ["JUNK", "bext", "ubxt", "chna", "axml"] # Non-BW64 - Note chna and adm MUST be present together - making a rule # TODO: define JUNK, bext ubxt - look up purpose, define rules
if outerChunkIdObj["value"] == "BW64":
    optionalInnerChunks = ["chna", "axml"] # Note chna and adm MUST be present together - making a rule

axmlPresence = (innerChunks["axml"]["chunkStart"] is not None)
chnaPresence = (innerChunks["chna"]["chunkStart"] is not None)
notesOutput = []

for chunkName in innerChunks:
    heading = "Chunk " + chunkName.upper() + " Present"
    thisPresence = (innerChunks[chunkName]["chunkStart"] is not None)

    if chunkName in mandatoryInnerChunks:
        o(heading, thisPresence,  thisPresence, "chunk is mandatory for this file type")

    elif chunkName in optionalInnerChunks:
        if chunkName == "axml" or chunkName == "chna":
            o(heading, thisPresence,  axmlPresence==chnaPresence, "chunk is optional but axml and chna must be together")
        else:
            o(heading, thisPresence,  True, "chunk is optional for this file type")

    else:
        o(heading, thisPresence,  not thisPresence, "chunk not expected for this file type")

    if not thisPresence:
        for tagMatchPos in innerChunks[chunkName]["tagMatchPositions"]:
            overlappingChunk = "Outer Chunk header"
            for olChunk in chunkOrder:
                if innerChunks[olChunk]["chunkStart"] < tagMatchPos:
                    overlappingChunk = olChunk.upper() + " chunk"
                else:
                    break
            notesOutput.append("Potential " + chunkName.upper() + " chunk start found at file position " + str(tagMatchPos) + " but this is overlapped by the " + overlappingChunk + ".")

if len(notesOutput) > 0:
    print
    for note in notesOutput:
        print "   Note: " + note
    print


# Validate sequence of inner chunks

print "\nINNER CHUNK SIZES AND SEQUENCE\n"

print "   Note: Chunk order is " + str(chunkOrder) + "\n"

lastChunkName = "Outer Chunk"
lastChunkEnd = 0 # Needs to be everything up to the inner chunks!
for varObj in outerChunk["structure"]:
    if varObj["varType"] == "chunks" or "varSize" not in varObj:
        break
    lastChunkEnd = lastChunkEnd + varObj["varSize"]

i = 0
while i<=len(chunkOrder):   # This will perform one extra check for alignment with outer chunk end

    #   Revert to outer chunk end pos for final check
    thisChunkName = "Outer Chunk End"
    thisChunkPos = outerChunk["chunkEnd"]
    thisChunkEnd = outerChunk["chunkEnd"]
    if i<len(chunkOrder):
        thisChunkName = chunkOrder[i].upper()
        thisChunkPos = innerChunks[chunkOrder[i]]["chunkStart"]
        thisChunkEnd = innerChunks[chunkOrder[i]]["chunkEnd"]
    heading = lastChunkName + " to " + thisChunkName + " gap"

    value = thisChunkPos- lastChunkEnd
    desc = "perfectly sequential/aligned"
    if value > 0:
        desc = str(value) + " byte gap between " + lastChunkName + " and " + thisChunkName
    elif value < 0:
        desc = str(abs(value)) + " byte overlap between " + lastChunkName + " and " + thisChunkName

    o(heading, value, (value==0), desc)

    lastChunkName = thisChunkName
    lastChunkEnd = thisChunkEnd
    i = i+1

# Validate properties in inner chunks

for chunkName in innerChunks:

    if innerChunks[chunkName]["chunkStart"] is None:
        continue

    print "\n\nINNER CHUNK: " + chunkName + "\n"

    chunkObj = innerChunks[chunkName]

    # First, start and end info!
    o("Start Position", chunkObj["chunkStart"])
    o("Header Size", chunkObj["chunkHeaderSize"])
    errorDesc = None
    if chunkObj["chunkOwnLength"] is not None and chunkObj["chunkDs64Length"] is not None:
        errorDesc = "size specified by both self and ds64 table"
    if chunkObj["chunkOwnLength"] is None and chunkObj["chunkDs64Length"] is None:
        errorDesc = "no size specified anywhere for this chunk"
    chunkSizeObj = getObjFromArray(chunkObj["structure"], "varType", "ckSize")
    chunkSizeReport = chunkSizeObj["value"]
    if chunkSizeReport is not None:
        chunkSizeReport = reportLe(chunkSizeObj["content"], (chunkSizeReport==-1))
    o("Self-Stated Size (chunkSize)", chunkSizeReport, (errorDesc is None), errorDesc)
    ds64SizeReport = chunkObj["chunkDs64Length"]
    if chunkObj["chunkDs64Length"] is not None:
        if chunkName == "data":
            o("DS64 Stated Size", reportLe(ds64DataSize), (errorDesc is None), errorDesc)
        else:
            o("DS64 Table Stated Size", reportLe(ds64TableEntries[chunkName]), (errorDesc is None), errorDesc)
    o("End Position (implied)", chunkObj["chunkEnd"])

    # Any other Dims validation
    chunkLen = None
    if chunkObj["chunkDs64Length"] is not None:
        chunkLen = chunkObj["chunkDs64Length"]
    if chunkObj["chunkOwnLength"] is not None:
        chunkLen = chunkObj["chunkOwnLength"]

    minSize = 0
    for varObj in chunkObj["structure"]:
        if "mandatory" in varObj and varObj["mandatory"] is True:
            if "varSize" in varObj:
                minSize = minSize + varObj["varSize"]
            elif "varMinSize" in varObj and varMinSize is not None:
                minSize = minSize + varObj["varMinSize"]
    minSize = minSize - chunkObj["chunkHeaderSize"] # Size should exclude header

    o("Length (implied)", chunkLen, (chunkLen is not None and chunkLen >= minSize), "expecting size >= " + str(minSize) + " bytes (mandatory params)")

    # Chunk-specific validation

    if chunkName == "ds64":

        # Vars

        bw64SizeObj = getObjFromArray(chunkObj["structure"], "varName", "bw64Size")
        dataSizeObj = getObjFromArray(chunkObj["structure"], "varName", "dataSize")
        dummyObj = getObjFromArray(chunkObj["structure"], "varName", "dummy")
        tableLengthObj = getObjFromArray(chunkObj["structure"], "varName", "tableLength")
        tableObj = getObjFromArray(chunkObj["structure"], "varName", "table")

        heading = "Chunk bw64Size Parameter"
        if bw64SizeObj["contentLength"] is not None:
            o(heading, reportLe(bw64SizeObj["content"]), True)
        else:
            o(heading, reportLe(bw64SizeObj["content"]), False, "could not read value")

        heading = "Chunk dataSize Parameter"
        if dataSizeObj["contentLength"] is not None:
            o(heading, reportLe(dataSizeObj["content"]), True)
        else:
            o(heading, reportLe(dataSizeObj["content"]), False, "could not read value")

        heading = "Chunk dummy Parameter"
        if dummyObj["contentLength"] is not None:
            o(heading, reportLe(dummyObj["content"]), (dummyObj["value"]==0), "expect dummy value to be 0")
        else:
            o(heading, reportLe(dummyObj["content"]), False, "could not read value")

        # Try to detect number of actual table entries
        tableEntryCount = None
        tableRemainingBytes = None
        if tableObj["contentLength"] is not None:
            tableEntryCount = int(tableObj["contentLength"]/tableObj["varSizeMultiple"])
            tableRemainingBytes = tableObj["contentLength"]%tableObj["varSizeMultiple"]

        heading1 = "Chunk tableLength Parameter"
        heading2 = "Chunk table Parameter Size"

        if tableLengthObj["contentLength"] is None and tableObj["contentLength"] is None:
            # Both None
            o(heading1, None, False, "could not read value")
            o(heading2, None, False, "could not read value")
        elif tableObj["contentLength"] is None:
            # Just table None
            o(heading1, reportLe(tableLengthObj["content"]), None, "can not validate due to missing table")
            o(heading2, None, False, "could not read value")
        else:
            # Table is good, don't know about tableLength
            if tableLengthObj["contentLength"] is None:
                # Just table length None
                o(heading1, None, False, "could not read value")
            else:
                # Both populated
                o(heading1, reportLe(tableLengthObj["content"]), (tableEntryCount==tableLengthObj["value"]), "expected to match table entry count implied by table size")

            if tableRemainingBytes == 0:
                o(heading2, str(tableObj["contentLength"]) + " bytes", True, str(tableEntryCount) + " table entries of " + str(tableObj["varSizeMultiple"]) + " bytes each")
            else:
                o(heading2, str(tableObj["contentLength"]) + " bytes", False, "table size must be a multiple of " + str(tableObj["varSizeMultiple"]))

        # Table Entries
        heading = "Table Entry - chunkId"
        for tableEntryChunkId in ds64TableEntries:
            if tableEntryChunkId in innerChunks:
                if innerChunks[tableEntryChunkId]["chunkStart"] is None:
                    o(heading, tableEntryChunkId, False, "chunk not found in file")
                else:
                    o(heading, tableEntryChunkId, True, "chunk found in file")
            else:
                o(heading, tableEntryChunkId, False, "unrecognised chunkId")

        # Any other chunk-specific validation
        o("DS64 Table Self-Entry", (chunkObj["chunkDs64Length"] is not None), (chunkObj["chunkDs64Length"] is None), "ds64 can not specify its size in its own table")

    elif chunkName == "fmt":
        # Vars

        formatTagObj = getObjFromArray(chunkObj["structure"], "varName", "formatTag")
        channelCountObj = getObjFromArray(chunkObj["structure"], "varName", "channelCount")
        sampleRateObj = getObjFromArray(chunkObj["structure"], "varName", "sampleRate")
        bytesPerSecondObj = getObjFromArray(chunkObj["structure"], "varName", "bytesPerSecond")
        blockAlignmentObj = getObjFromArray(chunkObj["structure"], "varName", "blockAlignment")
        bitsPerSampleObj = getObjFromArray(chunkObj["structure"], "varName", "bitsPerSample")
        cbSizeObj = getObjFromArray(chunkObj["structure"], "varName", "cbSize")
        extraDataObj = getObjFromArray(chunkObj["structure"], "varName", "extraData")

        heading = "Chunk formatTag Parameter"
        if formatTagObj["contentLength"] is not None:
            o(heading, reportLe(formatTagObj["content"]), (formatTagObj["value"]==1), "expect 0x0001 for WAVE_FORMAT_PCM")   # TODO: Check - is this mandatory?
        else:
            o(heading, reportLe(formatTagObj["content"]), False, "could not read value")

        heading = "Chunk channelCount Parameter"
        if channelCountObj["contentLength"] is not None:
            o(heading, reportLe(channelCountObj["content"]), True)
        else:
            o(heading, reportLe(channelCountObj["content"]), False, "could not read value")

        heading = "Chunk sampleRate Parameter"
        if sampleRateObj["contentLength"] is not None:
            o(heading, reportLe(sampleRateObj["content"]), True)
        else:
            o(heading, reportLe(sampleRateObj["content"]), False, "could not read value")

        heading = "Chunk bytesPerSecond Parameter"
        if bytesPerSecondObj["contentLength"] is not None:
            if type(channelCountObj["value"])==int and type(sampleRateObj["value"])==int and type(bitsPerSampleObj["value"])==int:
                expectedBps = channelCountObj["value"] * sampleRateObj["value"] * bitsPerSampleObj["value"] / 8
                o(heading, reportLe(bytesPerSecondObj["content"]), (bytesPerSecondObj["value"]==expectedBps), "should be chns*sr*bits/8 = " + str(expectedBps)) # TODO: Only important for compressed formats so really mandatory here?
            else:
                o(heading, reportLe(bytesPerSecondObj["content"]), None, "cannot check - missing data (should be chns*sr*bits/8)") # TODO: Only important for compressed formats so really mandatory here?
        else:
            o(heading, reportLe(bytesPerSecondObj["content"]), False, "could not read value")

        heading = "Chunk blockAlignment Parameter"
        if blockAlignmentObj["contentLength"] is not None:
            if type(channelCountObj["value"])==int and type(bitsPerSampleObj["value"])==int:
                expectedBa = channelCountObj["value"] * bitsPerSampleObj["value"] / 8
                o(heading, reportLe(blockAlignmentObj["content"]), (blockAlignmentObj["value"]==expectedBa), "should be chns*bits/8 = " + str(expectedBa))
            else:
                o(heading, reportLe(blockAlignmentObj["content"]), None, "cannot check - missing data (should be chns*bits/8)")
        else:
            o(heading, reportLe(blockAlignmentObj["content"]), False, "could not read value")

        heading = "Chunk bitsPerSample Parameter"
        if type(bitsPerSampleObj["value"])==int:
            o(heading, reportLe(bitsPerSampleObj["content"]), (bitsPerSampleObj["value"]%8==0), "expect multiple of 8") # TODO: Strictly true??
        else:
            o(heading, reportLe(bitsPerSampleObj["content"]), True, "could not read value (optional anyway)")

        heading1 = "Chunk cbSize Parameter"
        heading2 = "Chunk extraData Parameter Size"

        if cbSizeObj["contentLength"] is None and extraDataObj["contentLength"] is None:
            # Both None
            o(heading1, None, True, "could not read value (optional anyway)")
            o(heading2, None, True, "could not read value (optional anyway)")
        elif cbSizeObj["contentLength"] is not None and extraDataObj["contentLength"] is not None:
            # Both populated
            if outerChunkIdObj["value"] == "BW64":
                o(heading1, reportLe(cbSizeObj["content"]), (cbSizeObj["value"]==0), "cbSize should be 0 for BW64 (no extraData)")
            else:
                o(heading1, reportLe(cbSizeObj["content"]), (cbSizeObj["value"]==extraDataObj["contentLength"]), "cbSize should match length of extraData")
            o(heading2, extraDataObj["contentLength"], (cbSizeObj["value"]==extraDataObj["contentLength"]), "cbSize should match length of extraData")
        elif cbSizeObj["contentLength"] is not None:
            # Just cbSize populated
            o(heading1, reportLe(cbSizeObj["content"]), (cbSizeObj["value"]==0), "extraData missing, so expecting cbSize==0")
            o(heading2, None, True, "could not read value (optional anyway)")
        else:
            # Just extraData populated
            o(heading1, None, False, "could not read value, but we have extraData")
            o(heading2, extraDataObj["contentLength"], None, "can not validate due to missing cbSize")

        # Any other chunk-specific validation

    elif chunkName == "data":

        waveDataObj = getObjFromArray(chunkObj["structure"], "varName", "waveData")
        heading = "Chunk waveData Parameter Size"
        if waveDataObj["contentLength"] is not None:
            if innerChunks["fmt"]["chunkStart"] is not None:
                channelCountObj = getObjFromArray(innerChunks["fmt"]["structure"], "varName", "channelCount")
                bitsPerSampleObj = getObjFromArray(innerChunks["fmt"]["structure"], "varName", "bitsPerSample")
                if type(channelCountObj["value"])==int and type(bitsPerSampleObj["value"])==int:
                    chnsAndBits = channelCountObj["value"] * bitsPerSampleObj["value"] /8
                    o(heading, waveDataObj["contentLength"], (waveDataObj["contentLength"]%chnsAndBits==0), "should be divisible by (chns*bits/8) = " + str(chnsAndBits))
                else:
                    o(heading, waveDataObj["contentLength"], None, "cannot check - missing fmt data (should be divisible by (chns*bits/8))")
            else:
                o(heading, waveDataObj["contentLength"], None, "cannot check - missing fmt chunk (should be divisible by (chns*bits/8))")
        else:
            o(heading, None, False, "could not read value")

    elif chunkName == "chna":

        numTracksObj = getObjFromArray(chunkObj["structure"], "varName", "numTracks")
        heading = "Chunk numTracks Parameter"
        if type(numTracksObj["value"])==int:
            if innerChunks["fmt"]["chunkStart"] is not None:
                channelCountObj = getObjFromArray(innerChunks["fmt"]["structure"], "varName", "channelCount")
                if type(channelCountObj["value"])==int:
                    o(heading, reportLe(numTracksObj["content"]), (numTracksObj["value"]<=channelCountObj["value"]), "should be <= chns")
                else:
                    o(heading, reportLe(numTracksObj["content"]), None, "cannot check - missing fmt data (should be <= chns)")
            else:
                o(heading, reportLe(numTracksObj["content"]), None, "cannot check - missing fmt chunk (should be <= chns)")
        else:
            o(heading, None, False, "could not read value")

        # - it is possible to have multiple UIDs for each track
        numUIDsObj = getObjFromArray(chunkObj["structure"], "varName", "numUIDs")
        heading = "Chunk numUIDs Parameter"
        if numUIDsObj["contentLength"] is not None:
            o(heading, reportLe(numUIDsObj["content"]), True)
        else:
            o(heading, None, False, "could not read value")

        # - The number of ID structures must be equal to or greater than the number of track UIDs used
        # - The audioID structure contains an index to the track used in the <data> chunk (which contains the audio samples), starting with the value of 1 for the first track
        # - When an ID is not being used the trackIndex should be given the value of zero

        IDObj = getObjFromArray(chunkObj["structure"], "varName", "ID")
        heading = "Chunk ID Parameter Size"
        if IDObj["contentLength"] is not None:
            numIDEntries = int(IDObj["contentLength"]/IDObj["varSizeMultiple"])
            numIDEntriesRem = IDObj["contentLength"]%IDObj["varSizeMultiple"]
            # First check its a multiple of 40
            if numIDEntriesRem == 0:
                # Then is numIDEntries >= UIDs?
                if type(numUIDsObj["value"])==int:
                    o(heading, IDObj["contentLength"], (numIDEntries >= numUIDsObj["value"]), "number of ID chunks should be >= numUIDs")

                else:
                    o(heading, IDObj["contentLength"], None, "cannot check - numUIDs parameter missing")
            else:
                o(heading, IDObj["contentLength"], False, "size should be divisible by ID chunk size (" + str(IDObj["varSizeMultiple"]) + ")")
        else:
            o(heading, None, False, "could not read value")

        # Are the trackIndexes >= 0 and <= numTracks?
        trackIndexObj = getObjFromArray(chunkObj["innerChunks"]["ID"]["structure"], "varName", "trackIndex")
        heading = "Chunk ID trackIndex Parameters"
        indexCount = 0
        erroredIndexCount = 0
        firstErroredIndex = None
        firstErroredIndexPos = None

        i = 0
        while i+trackIndexObj["varSize"] <= IDObj["contentLength"]:
            # TODO: we can validate against AXML here later!
            indexCount = indexCount + 1
            tiContent = IDObj["content"][i:i+trackIndexObj["varSize"]]
            tiValue = leToInt(tiContent)
            if type(numTracksObj["value"])==int:
                if tiValue < 0 or tiValue > numTracksObj["value"]:
                    erroredIndexCount = erroredIndexCount + 1
                    if firstErroredIndex is None:
                        firstErroredIndex = reportLe(tiContent)
                        firstErroredIndexPos = indexCount

            i = i + IDObj["varSizeMultiple"]

        if type(numTracksObj["value"])==int:
            resultText = "(" + str(erroredIndexCount) + "/" + str(indexCount) + " index errors)"
            if erroredIndexCount == 0:
                o(heading, resultText, True, "all indexes valid", True) # True = trim value
            elif erroredIndexCount == 1:
                o(heading, resultText, False, "entry number " + str(firstErroredIndexPos) + ", value: " + firstErroredIndex)
            else:
                o(heading, resultText, False, "starting at entry " + str(firstErroredIndexPos) + ", value: " + firstErroredIndex)
        else:
            o(heading, "(" + str(indexCount) + " entries)", None, "cannot check - numTracks parameter missing")

    elif chunkName == "JUNK":

        chunkDataObj = getObjFromArray(chunkObj["structure"], "varName", "chunkData")
        heading = "Chunk chunkData Parameter Size"
        if chunkDataObj["contentLength"] is not None:
            minSize = chunkDataObj["varSizeMin"]
            if minSize is None:
                minSize = 0
            o(heading, chunkDataObj["contentLength"], (chunkDataObj["contentLength"]>=minSize), "min " + str(minSize) + " bytes to allocate ds64 space")
        else:
            o(heading, None, False, "could not read value")


    else:
        print "\n   Note: No validation rules set for this chunk"


print "\n"

cycleCount = 0

def ExpandList(inList):
    pass

def CollapsePoints2D(a1, a2):
    #take 2 arrays, X&Y, and return single list of points
    #can be replaced by python's zip function
    outArray = []
    if len(a1)==len(a2):
        for i in range(len(a1)):
            outArray.append((a1[i],a2[i]))
        return outArray

def ExpandPoints2D(inPnts):
    #take a single list of 2D points and expand to 2 sets of lists
    #can also be replaced by pythons zip function
    #http://stackoverflow.com/questions/19339/a-transpose-unzip-function-in-python-inverse-of-zip
    xOut = []
    yOut = []
    for i in inPnts:
        xOut.append(i[0])
        yOut.append(i[1])
    return xOut, yOut

def Distance(p0, p1):
    #basic distance formula
    #can (likely) be replaced by math.hypot
    from math import sqrt
    return sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def ComboDistance(inXY):
    #output an array with ID, X, Y, and distance for all combinations
    from itertools import combinations
    lclCombo = combinations(inXY,2)
    outPut = []
    #return lclCombo

    for i in lclCombo:
        outPut.append((i[0],i[1],Distance(i[0],i[1])))
    outPut = sorted(outPut, key=lambda x:x[2])
    return outPut

def ChainedLinks(inLink):
    #Step 1: find Linked() links
    #permute inputs?
    from itertools import combinations
    lclList = []
    comBos = combinations(inLink, 2)
    for item in comBos:
        if Linked(item[0], item[1]):
            lclList.append(item)
    return lclList
    #lclList now holds all your chainable things...
    pass

#This function is just to prep the output from chainedLinks
#to keep the recursion in Chaining simpler... I hope.
#no recursion here...

def ChainPrep(inPairs):
    #convert everything to local lists... its just easier
    lclList = []
    for pair in inPairs:
        lclPair = []
        for link in pair:
            lclLink = list(link)
            lclPair.append(lclLink)
        lclList.append(lclPair)
    #next step is to sort, but test first...
    return lclList


def Chaining(inLinks, test_back=[]):
    """
    Testing/converting test_back data:
    """
    #check length of "test_back" if > 0 then convert data to LINK-OVERLAP form:
    if len(test_back)>0:
        pass
        #do this as a seperate function!



    from itertools import groupby
    #this global variable may be sloppy, but it worked.
    global cycleCount

    ##First run only?
    if True: #cycleCount == 0:
        #All items are at least chains of 2 links, look for longer chains
        #using duplicate nodes:
        lclAllLinks = []
        for pair in inLinks:
            for link in pair:
                lclAllLinks.append(list(link))
        #now, sort list and count links:
        lclAllLinks.sort()
        #this is needed to handle the counts situation...
        #list comprehension?
        unDupeLinks = []
        for temp in lclAllLinks:
            if temp not in unDupeLinks:
                unDupeLinks.append(temp)

        #below holds counts that hold the same index as the sorted above
        lclCounts = [len(list(group)) for key, group in groupby(lclAllLinks)]
        #print "Links", unDupeLinks
        #print "Counts", lclCounts
        chainKeys = []

        #enumerate might have been handy to use here, lessons learned.
        for idx in range(len(lclCounts)):
            if lclCounts[idx] > 1:
                #print unDupeLinks[idx], " must be chained!"
                chainKeys.append(unDupeLinks[idx])

        if cycleCount > 0:
            #print "UnDupeLinks:", unDupeLinks
            #print "lclCounts:", lclCounts
            pass
    #if cycleCount == 0:print " First Cycle!"

    cycleCount = cycleCount + 1
    if cycleCount > 500:
        print "recursion count for current call:", 500
        return "Too many points input for function, define higher cut_off"
        #raise("early out error")
    exitFlag = True
    for count2 in lclCounts:
        if count2 > 1:
            exitFlag = False
    if exitFlag == True:
        cycleCount = 0
        return inLinks


    #This is the heart of the chaining algorithm, everything else is just setup...
    ##All Runs?
    cycleCount = cycleCount + 1
    if cycleCount > 0:
        if inLinks == test_back:
            #print "BREAK!!!"
            #test_back allows for recursion but also is used for knowing when to exit, i think?

            return inLinks
        else:
            #I wrote this before I knew about dictionaries, list comprehension, enumerate, and a few other 
            #helper functions.


            localChains = []
            exitChain = []

            #for this part, you've correctly merged 2 chains, first add the straglers
            #the chains of 2, those without keys
            localChains2 = []
            #print "key", chainKeys[0]
            tempChain = []
            #rewrite to handle first key only:
            for Links in inLinks:
                if chainKeys[0] not in Links:
                    localChains2.append(Links)
            for chain in localChains2:
                localChains.append(chain)
            #print "chains part"
            #for i in localChains: print i
            #print '\n'

            for Links in inLinks:
                if chainKeys[0] in Links:
                    tempChain.append(Links)
            #print "chain extension:"
            #for i in tempChain:print i
            #print '\n'
            ##########
            for temp in tempChain:

                nTemp = []#temp.remove(key)
                for t in temp:
                    if t != chainKeys[0]:
                        nTemp.append(t)
                #print "temp", temp, "nTemp", nTemp
                for linkAx in nTemp:
                    exitChain.append(linkAx)
            ##########
            exitChain.append(chainKeys[0])
            #print "exit chain"
            #print exitChain
            localChains.append(exitChain)

            returnChains = localChains

            #if cycleCount%50==0:print "Recursion Count:", cycleCount # "!!!!!!!  Process Recursion count +50  !!!!!!!"
            return Chaining(returnChains, inLinks)







#this function takes two links as inputs,
#return true if the cross and false if they don't
def Linked(inLink1, inLink2):
    testResult = False
    for node in inLink1:
        if node in inLink2:
            testResult = True
    return testResult

#this function tests to see if two linked links are hangers or joiners
###I had to develope an interval terminology set, hangers = hanging links, joiners = joining links
#since you're using sets, try unioning your input sets with this test, see what hapens?
def JoiningLink(inLink1, inLinkSet):
    testResult = False
    part1 = False
    part2 = False
    joinedLinks = []

    node1 = list(inLink1)[0]
    node2 = list(inLink1)[1]
    for link in inLinkSet:
        if node1 in link:
            part1 = True
            joinedLinks.append(link)
        if node2 in link:
            part2 = True
            joinedLinks.append(link)
        #assume duplicates are screened out properly here...
    if part1 and part2:
        testResult = True, joinedLinks
        return testResult
    else:
        return False,False

def SetReversion(inChainsList):
    from sets import Set
    outSets = Set()
    for chain in inChainsList:
        outChain = Set()
        for link in chain:
            outLink = Set(link)
            outChain.add(outLink)
        outSets.add(outChain)
    return outSets

#I believe this is the function I needed to solve my problem of building networks,
#everythng else was prep to make this possible in a semi-controlable way

def MinChainDistanceGeom(inDistCombo, total_points, average_multiple = None, print_flag =False, cut_off=150):
    #there appears to be a bug in the return value of nodeset when average_multiple is used
    #work around involves deriving nodeset from allLinks
    curDist = inDistCombo
    #number of points in universe subset, used to abort early when needed
    totalPoints = total_points

    try:
            if int(str(totalPoints))>cut_off:
                print "Too many points input for function, define higher cut_off"
                print "number of points:", int(str(totalPoints))
                return "Too many points input for function, define higher cut_off"
    except:
            pass

    from sets import Set
    #control variables
    runCount = 0
    oidCount = 0
    globalChainID = 0
    #you need listLinks, the list version of allLinks,
    #to maintain the order for distance
    listLinks = []
    #you get four, and only four, link containers:
    allLinks = Set()
    orphanLinks = Set()
    hangingLinks = Set()
    joiningLinks = Set()
    #and one to hold chainSets
    chainSets = Set()
    #one more to hold nodes
    nodeSet = Set()

    breakCount = 0
    if print_flag:
            print "Total Points", totalPoints

    #running average numbers:
    #runTotal = len(allLinks), find as needed
    runTotal = 0
    runDistance = 0.0
    runAverage = 0.0 #runDistance/runTotal
    """
    copy and paste for each instance:
    runTotal = runTotal + 1
    runDistance = runDistance + pair.DISTANCE
    runAverage = runDistance/runTotal

    """
    for pair in curDist:
        #Assume x = 0, y = 1, distance = 2
        #early break logic if pair.DISTANCE is bigger than average_multiple * runAverage:
        #average_multiple defaults to none, and None>int() is always false
        if average_multiple>0:
            if float(pair[2]) > runAverage * average_multiple and len(allLinks)>=1:
                if print_flag:
                    print "distance:", pair[2], "average", runAverage
                    print "runDistance", runDistance, "runTotal", runTotal
                #exit with results:
                return orphanLinks, hangingLinks, joiningLinks, allLinks, SetReversion(Chaining(ChainPrep(ChainedLinks(allLinks)))), nodeSet, runAverage


        oidCount = oidCount + 1
        if oidCount%100 == 0 and print_flag:
            print "processed ", oidCount, " pairs"
        #run trap.
        if len(allLinks)>=int(str(totalPoints))-1:
            continue
        #print "chain count", len(allLinks)
        linkType = None
        oidCount = oidCount + 1
        currentLink = Set([pair[0],pair[1]])

        #print oidCount, pair.INPUT_FID, pair.NEAR_FID
        #Weed out the junk.  This gets more complicated...
        if currentLink in allLinks:
            continue


        #Node Check, don't doublecount nodes..
        if pair[0] in nodeSet and pair[1] in nodeSet:
            #must be joining link!???
            #need to make sure redundant joins aren't introduced.
            #thats likely where chaining comes into play
            lclJoin = JoiningLink(currentLink, allLinks)
            if lclJoin[0]:
                pass
                #print lclJoin[1]
            #check the chainSets() for issues
            #at the moment, I need to manually reset cycleCount
            cycleCount = 0
            #print "disance for recursion join:", pair.DISTANCE
            preChainSets = SetReversion(Chaining(ChainPrep(ChainedLinks(allLinks))))

            #regenerate chainSets


            #test for corupt chans by looking to see if the joinLink's
            #nodes are already fully represented in each individual chain
            #if both currentLink-Join nodes are already in the chain, reject the current link
            keepJoin = True
            lclNodes0 = Set()
            for chain in preChainSets:
                lclNodes1 = Set()
                for link in chain:
                    for node in link:
                        lclNodes1.add(node)
                if pair[0] in lclNodes1 and pair[1] in lclNodes1:
                    keepJoin = False

            if keepJoin == False:
                #if you get here, you've rejected the join
                #raise("break again!")
                continue
            #do you accept this join?
            if print_flag:
                print "Joining link!","chain count:", len(allLinks), "out of", totalPoints
            joiningLinks.add(currentLink)
            allLinks.add(currentLink)
            listLinks.append(currentLink)
            runTotal = runTotal + 1
            runDistance = runDistance + pair[2]
            runAverage = runDistance/runTotal

            #raise("break again!")
            continue
        nodeSet.add(pair[0])
        nodeSet.add(pair[1])


        #Test for hanging link:
        tempLinks = []
        tCount = 0
        for link in allLinks:
            if Linked(link, currentLink):
                #this has to be a hanging link, joining links won't pass "Linked" test
                subLink = link
                hangingLinks.add(currentLink)
                tempLinks.append(currentLink)
                #Logic breaks for loop: fix with tempLinks...
                #allLinks.add(currentLink)
                if print_flag:
                    print "Hanging Link:", currentLink,"chain count:", len(allLinks), "out of", totalPoints#, "connected to:", link
                tCount = tCount+1
                #this criteria likely indicates a branch
                if tCount > 1:
                    pass

                    #raise('issue')

                linkType = "Hanging"
        if linkType == "Hanging":
            runTotal = runTotal + 1
            runDistance = runDistance + pair[2]
            runAverage = runDistance/runTotal
            for tempLink in tempLinks:
                allLinks.add(tempLink)
                listLinks.append(tempLink)
            try:del tempLink, tempLinks
            except:pass



        #Deal with chaining:
        #hanging Chains should be easier...
        if linkType == "Hanging":
            chainSets.add(Set([currentLink, Set(subLink)]))
            breakCount = breakCount +1
            if breakCount > 150:
                pass
                #raise("break")
            #raise("later")



        elif linkType == "Joining":
            print "possibly more complicated"
            raise("later")

        #Add new orphans, this should be easy and fool proof
        #It is assumed if a pair gets this far its an orphan, but tst anyway, eventually
        #this assumption is apparently wrong...
        if currentLink not in allLinks:
            orphanLinks.add(currentLink)
            allLinks.add(currentLink)
            listLinks.append(currentLink)
            runTotal = runTotal + 1
            runDistance = runDistance + pair[2]
            runAverage = runDistance/runTotal
            if print_flag:
                print "Orphan Link:", currentLink,"Link count:", len(allLinks), "out of", totalPoints

    return orphanLinks, hangingLinks, joiningLinks, allLinks, SetReversion(Chaining(ChainPrep(ChainedLinks(allLinks)))), nodeSet, runAverage


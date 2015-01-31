import os,sys
import matplotlib.pyplot as plt, numpy as np, pickle
import matplotlib.animation as animation
from SetLib import *

def Distance(p0, p1):
    #basic distance formula
    from math import sqrt
    return sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

#i did not include sample data, which in retrospect is a mistake.  generally speaking the inputs
#are just a set of cordinate pairs, based on code below a list of x coordinates, y coordinates
#and whatever data structre is loaded to lclSets below.

#lclSets should be a list of point-pair sets, likely built from xIn and yIn?


setGroups = open(r'setGroupData.pkl','r')



#load stored data
lclSets, xIn, yIn = pickle.load(setGroups)

"""
print "generate master chain set"
#recreate whole branch network:
tempXY = zip(xIn,yIn)
Combo1 = ComboDistance(tempXY)
cycleCount = 0
lpChainSet = MinChainDistanceGeom(Combo1, len(xIn), print_flag = False)
mstrChain = lpChainSet[3]
print "chaing generation complete"
"""





printLabels = False
fig = plt.figure(figsize=(12,10))
saveFrames = []
ims = []

frameBase = plt.scatter(xIn, yIn, color = 'Blue', s=6, zorder=3)

font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }
"""
textOut = "Set ID:"
frameText = plt.text(-90,90, s="TEST TEXT!")
"""

for chain in lclSets:
    lclTotal = 0
    lclCount = 0
#animation rate:

    print "setID", chain[1], "length", len(chain[0])
    # THIS IS ORPHAN LOGIC!
    # might need to ad type(list(chain[0])[0]) is tuple
    # logic, check out what happens with chains of 3, i.e. 2 links should look the same as 2 points.
    if len(chain[0])==2 and type(list(chain[0])[0]) is tuple:
        # Text to Display!
        linePoints = list(chain[0])
        lclCount = lclCount + 1
        curDist = Distance(linePoints[0],linePoints[1])
        lclTotal = lclTotal + curDist
        for i in range(15):
            #print "\t this is an orphan"
            #plot orphan lines as red
            linePoints = list(chain[0])
            if printLabels:plt.text(linePoints[0][0],linePoints[0][1], chain[1])
            #remember, for some reason plt.plot returns a list?
            curFrame = plt.plot([linePoints[0][0],linePoints[1][0]], [linePoints[0][1],linePoints[1][1]], color = 'red',linewidth=2, zorder =2, alpha=((i+1.0)/15))[0]
            #add base, current iteration, and past iterations for each frame
            imFrames = []
            imFrames.append(curFrame)
            imFrames.append(frameBase)
            # Text to Display!
            
            
            #only increment once per line, not once per animated frame!
            #lclTotal = lclTotal + curDist
            #lclCount = lclCount + 1
            lclAvg = lclTotal/lclCount
            textOut = "Set ID: " +str(chain[1])+"  Link Count :"+str(lclCount)+"/1 Running Average: "+str(round(lclAvg,2))
            frameText = plt.text(-90,140, s=textOut)
            imFrames.append(frameText)
            # end text display
            imFrames.append(frameText)
            imFrames.extend(saveFrames)
            ims.append(imFrames)
            #raise('check')
        saveFrames.append(curFrame)
        
    else:# len(chain[0])>2:
        print "\t this is a chain"
        #chain[0] is stored as chained links, no MinChainDistanceGeom call required!
        #convert to plt.plot(xList,yList) form
        lclX = []
        lclY = []
        #need to sort chain[0] by distance!
        # see previous animation example for this!
        # reference DemoPointSetMaker_2.5, around line 80:
        preSortList = []
        for pair in chain[0]:
            tList = list(pair)
            row = [tList[0],tList[1],Distance(tList[0],tList[1])]
            preSortList.append(row)

        sortList = sorted(preSortList, key=lambda x:x[-1])
        sortList2 = []
        for x in sortList:
            sortList2.append([x[0],x[1]])        
        #moddified following line to feed from sortList2 instead of chain[0]
        #for link in chain[0]:
        for link in sortList2:
            # Text to Display!
            linePoints = list(link)
            lclCount = lclCount + 1
            curDist = Distance(linePoints[0],linePoints[1])
            lclTotal = lclTotal + curDist
            for i1 in range(15):
                imFrames = []
                
                
                            
                linePoints = list(link)
                if printLabels:plt.text(linePoints[0][0],linePoints[0][1], chain[1])
                
                curFrame = plt.plot([linePoints[0][0],linePoints[1][0]], [linePoints[0][1],linePoints[1][1]], color = 'green',linewidth=2, zorder =1,alpha=((i1+1.0)/15))[0]
                #add base, current iteration, and past iterations for each frame
                # Text to Display!
                curDist = Distance(linePoints[0],linePoints[1])
                
                #only increment once per line, not once per animated frame!
                #lclTotal = lclTotal + curDist
                #lclCount = lclCount + 1
                lclAvg = lclTotal/lclCount
                textOut = "Set ID:" +str(chain[1])+"  Link Count: "+str(lclCount)+"/"+str(len(sortList2)) +" Running Average: "+str(round(lclAvg,2))
                frameText = plt.text(-90,140, s=textOut)
                imFrames.append(frameText)
                # end text display                
                imFrames = []
                imFrames.append(curFrame)
                imFrames.append(frameText) 
                imFrames.append(frameBase)
                imFrames.extend(saveFrames)
                ims.append(imFrames)
            saveFrames.append(curFrame)
            
            

        
ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,repeat_delay=1000) 

print "saving file now..."
#ani.save('setGroup.mp4',writer='mencoder',extra_args=['-ovc', 'x264'])

count = 0
for i in ims:
    i




plt.show()
plt.close()


print "\nDone!\n"

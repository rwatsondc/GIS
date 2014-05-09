import os,sys
import matplotlib.pyplot as plt, numpy as np, pickle
import matplotlib.animation as animation
from SetLib import *

def Distance(p0, p1):
    #basic distance formula
    from math import sqrt
    return sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

setGroups = open(r'setGroupData.pkl','r')



#load stored data
lclSets, xIn, yIn = pickle.load(setGroups)


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


#Setup master chaining demo data
tempXY = CollapsePoints2D(xIn,yIn)
Combo1 = ComboDistance(tempXY)
testChain = MinChainDistanceGeom(Combo1, len(xIn), print_flag =False, cut_off=250)

allLinks = testChain[3]

#now sort allLink, this is old hat...
preSortList = []
for pair in allLinks:
    tList = list(pair)
    row = [tList[0],tList[1],Distance(tList[0],tList[1])]
    preSortList.append(row)

sortList = sorted(preSortList, key=lambda x:x[-1])
sortList2 = []
for x in sortList:
    sortList2.append([x[0],x[1]])

#now print alls, in sort-distance order

for link in sortList2:
    for i in range(15):
        linePoints = list(link)
        curFrame = plt.plot([linePoints[0][0],linePoints[1][0]], [linePoints[0][1],linePoints[1][1]], color = 'green',linewidth=2, zorder =2, alpha=((i+1.0)/15))[0]
        #add base, current iteration, and past iterations for each frame
        imFrames = []
        imFrames.append(curFrame)
        imFrames.append(frameBase)
        imFrames.extend(saveFrames)
        ims.append(imFrames)

    saveFrames.append(curFrame)

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,repeat_delay=1000)



print "saving file now..."
#ani.save('ChainingMethod.mp4',writer='mencoder',extra_args=['-ovc', 'x264'])
print "done saving..."

plt.show()
plt.close()


print "\nDone!\n"

import numpy as np
import math as m
import random as ran
import pandas as pd

df = pd.read_excel (r'ProjectData1.xlsx')

# Set coordinates for ship deployment
CGbase = [0, 25.769799, -80.143978]

# Function for distance between coordinates using Haversine
def getDist(lat1, long1, lat2, long2) :

    #Convert to radians
    lat1 = m.radians(lat1)
    lat2 = m.radians(lat2)
    long1 = m.radians(long1)
    long2 = m.radians(long2)

    # Haversine Formula
    deltLat = lat1 - lat2
    deltLong = long1 - long2
    a = m.sin(deltLat/2)**2 + m.cos(lat1) * m.cos(lat2) * m.sin(deltLong/2)**2
    c = 2*m.asin(m.sqrt(a))

    # Radius of Earth in miles
    r = 3961

    # Distance
    dist = c*r
    return(dist)



# function to calculate total route distance
def routeDistance(routeSeq):

    dist = getDist(routeSeq[0][1],routeSeq[0][2],
                  (routeSeq[1][1] + routeSeq[1][2])/2,(routeSeq[1][3] + routeSeq[1][4]) / 2)
    for i in range(1,len(routeSeq)-1):
        z1La = (routeSeq[i][3] + routeSeq[i][4])/2
        z1Lo = (routeSeq[i][1] + routeSeq[i][2]) / 2
        z2La = (routeSeq[i+1][3] + routeSeq[i+1][4]) / 2
        z2Lo = (routeSeq[i+1][1] + routeSeq[i+1][2]) / 2

        dist = dist + getDist(z1La, z1Lo, z2La, z2Lo)

    return dist

#Function to identify how many "hot zones" the route runs through
def hotZones(RZones, HZones):
    count = 0
    for z in RZones:
        for i in range(0, len(HZones)):
            if(z[0] == HZones[i]):
                count = count + 1

    return count

#Results from Nearest Centroid Classifier
hoZones = [1, 2, 3, 4, 5, 21, 22, 23, 24, 25, 41, 42, 43, 44, 45, 61, 62, 63, 64, 65, 66, 81, 82, 83, 84, 85, 86, 101,
            102, 103, 104, 105, 106, 107, 121, 122, 123, 124, 125, 126, 127, 141, 142, 143, 144, 145, 146, 147, 148,
            161, 162, 163, 164, 165, 166, 167, 168, 181, 182, 183, 184, 185, 186, 187, 188, 201, 202, 203, 204, 205,
            206, 207, 208, 209, 221, 222, 223, 224, 225, 226, 227, 228, 229, 241, 242, 243, 244, 245, 246, 247, 248,
            249, 250, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 281, 282, 283, 284, 285, 286, 287, 288, 289,
            290, 291, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 321, 322, 323, 324, 325, 326, 327, 328,
            329, 330, 331, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 361, 362, 363, 364, 365, 366,
            367, 368, 369, 370, 371, 372, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393]


#Function to evaluate the route
def evaluate(x):
    eval = routeDistance(x)
    return eval

# Function to divide map into zones
def createZones(minLo, maxLo, minLa, maxLa, zLo, zLa) :

    # Set zone width and length
    latInc = (maxLa - minLa)/zLa
    lonInc = (maxLo - minLo)/zLo

    # Initialize list to hold zones
    z = []

    # Initialize minimum Latitude to set zone boundaries
    miLa = minLa

    # Create zones
    for i in range(0,zLa):
        # Set zone boundaries
        miLo = minLo
        maLa = miLa + latInc
        for j in range(0, zLo):
            maLo = miLo + lonInc
            newZ = [(zLo*i+j)+1, miLo, maLo, miLa, maLa]
            z.append(newZ)
            miLo = maLo
        miLa = maLa

    # Return list of zones
    return z


# Function to find zone (z) a point (x) lies in
def zoneFinder(z, x, inc) :

    i = 0
    for j in range(0, len(z)):

        if(x[0] > z[i][1] and x[0] <= z[i][2]):
            if(x[1] > z[i][3] and x[1] <= z[i][4]):
                zone = [i + 1, z[i][1], z[i][2], z[i][3], z[i][4]]
                return zone

            else:
                i += inc

        else:
            i += 1

    zone = [-100, 0,0.0,0]
    return zone

def initRoute(zones, Base, entryZone, incidentZone, rowInc):

    route = [Base, entryZone]
    j = entryZone[0]-1

    if(entryZone != incidentZone):
        for i in range(1, len(zones)) :

            if(route[i][1] == incidentZone[1]) :
                if(route[i][3] == incidentZone[3]):
                    return(route)
                else :
                    route.append(zones[j+rowInc])
                    j += rowInc
            else :
                route.append(zones[j+1])
                j += 1

    else:
        return route


def neighborhood(zones, route, rowInc, colInc) :
    neighbors = []

    for i in range(2, len(route) - 1) :
        n1 = []
        n2 = []
        n3 = []
        n4 = []
        n5 = []

        for j in range(i) :
            n1.append(route[j])
            n2.append(route[j])
            n3.append(route[j])
            n4.append(route[j])
            n5.append(route[j])

        #Move up
        if (route[i-2][0] - route[i-1][0] != rowInc and route[i-1][0] != 0 % rowInc):
            z1 = route[i-1][0]+rowInc-1
            if (z1 < rowInc*colInc-1):
                n1.append(zones[z1])

                if(abs(zones[z1][0]-route[i+1][0]) != rowInc and abs(zones[z1][0]-route[i+1][0]) != rowInc + 1 and
                    abs(zones[z1][0]-route[i+1][0]) != 1 and abs(zones[z1][0]-route[i+1][0]) != rowInc - 1) :

                    if (abs(zones[z1][0]-route[i+1][0]) == rowInc - 2  or abs(zones[z1][0]-route[i+1][0])== rowInc + 2
                        or abs(zones[z1][0]-route[i+1][0]) == 2) :
                        n1.append(zones[z1+1])

                    else:
                        n1.append(zones[z1 - rowInc + 1])

                        if (abs(zones[z1][0]-route[i+1][0]) > 2*rowInc):
                            n1.append(zones[z1 - 2*rowInc + 1])

                n1L = len(n1)
                if (abs(n1[n1L - 1][0] - route[len(route) - 1][0]) != 1 and
                        abs(n1[n1L - 1][0] - route[len(route) - 1][0]) != rowInc - 1 and
                        abs(n1[n1L - 1][0] - route[len(route) - 1][0]) != rowInc and
                        abs(n1[n1L - 1][0] - route[len(route) - 1][0]) != rowInc + 1 and
                        abs(n1[n1L - 1][0] - route[len(route) - 1][0]) != 0):
                    for k in range(i + 1, len(route)-1) :
                        n1L = len(n1)

                        if(n1[n1L-1] != route[k] and n1[n1L-1] != route[k+1]):
                            n1.append(route[k])

                        n1L = len(n1)
                        if (abs(n1[n1L - 1][0] - route[len(route) - 1][0]) == 1 or
                                abs(n1[n1L - 1][0] - route[len(route) - 1][0]) == rowInc - 1 or
                                abs(n1[n1L - 1][0] - route[len(route) - 1][0]) == rowInc or
                                abs(n1[n1L - 1][0] - route[len(route) - 1][0]) == rowInc + 1 or
                                abs(n1[n1L - 1][0] - route[len(route) - 1][0]) == 0):
                            break

                if(n1[len(n1) - 1] != route[len(route) - 1]):
                    n1.append(route[len(route)-1])

                neighbors.append(n1)

        #Move diagonally up
        z2 = route[i-1][0]+rowInc
        if(z2 < rowInc*colInc-1 and route[i-1][0] != 0 % rowInc):
            n2.append(zones[z2])

            if(abs(zones[z2][0]-route[i+1][0]) != rowInc and abs(zones[z2][0]-route[i+1][0]) != 1 and
                abs(zones[z2][0]-route[i+1][0]) != rowInc - 1 and abs(zones[z2][0]-route[i+1][0]) != rowInc + 1):
                n2.append(zones[z2 - rowInc])

                if(abs(zones[z2][0]-route[i+1][0]) > 2*rowInc + 1):
                    n2.append(zones[z2 - 2*rowInc])

            n2L = len(n2)
            if (abs(n2[n2L - 1][0] - route[len(route) - 1][0]) != 1 and
                    abs(n2[n2L - 1][0] - route[len(route) - 1][0]) != rowInc - 1 and
                    abs(n2[n2L - 1][0] - route[len(route) - 1][0]) != rowInc and
                    abs(n2[n2L - 1][0] - route[len(route) - 1][0]) != rowInc + 1 and
                    abs(n2[n2L - 1][0] - route[len(route) - 1][0]) != 0):

                for k in range(i + 1, len(route)-1) :
                    n2L = len(n2)
                    if (n2[n2L - 1] != route[k] and n2[n2L - 1] != route[k+1]):
                        n2.append(route[k])

                    n2L = len(n2)
                    if (abs(n2[n2L - 1][0] - route[len(route) - 1][0]) == 1 or
                            abs(n2[n2L - 1][0] - route[len(route) - 1][0]) == rowInc - 1 or
                            abs(n2[n2L - 1][0] - route[len(route) - 1][0]) == rowInc or
                            abs(n2[n2L - 1][0] - route[len(route) - 1][0]) == rowInc + 1 or
                            abs(n2[n2L - 1][0] - route[len(route) - 1][0]) == 0):
                        break
            if(n2[len(n2) - 1] != route[len(route) - 1]):
                n2.append(route[len(route) - 1])

            neighbors.append(n2)

        #Move down
        z3 = route[i - 1][0] - rowInc - 1
        if (route[i-2][0] - route[i-1][0] != -rowInc and route[i-1][0] != 0 % rowInc):
            if (z3 >= 0):
                n3.append(zones[z3])
                if (abs(zones[z3][0]-route[i+1][0]) != 1  and abs(zones[z3][0]-route[i+1][0]) != rowInc and
                    abs(zones[z3][0]-route[i+1][0]) != rowInc - 1  and abs(zones[z3][0]-route[i+1][0]) != rowInc + 1):

                    if(abs(zones[z3][0]-route[i+1][0]) != rowInc - 2):
                        n3.append(zones[z3+1])

                    else:
                        n3.append(zones[z3 + rowInc + 1])
                        if(abs(zones[z3][0]-route[i+1][0]) >= 3 * rowInc):
                            n3.append(zones[z3 + 2*rowInc + 1])

                n3L = len(n3)
                if (abs(n3[n3L - 1][0] - route[len(route) - 1][0]) != 1 and
                        abs(n3[n3L - 1][0] - route[len(route) - 1][0]) != rowInc - 1 and
                        abs(n3[n3L - 1][0] - route[len(route) - 1][0]) != rowInc and
                        abs(n3[n3L - 1][0] - route[len(route) - 1][0]) != rowInc + 1 and
                        abs(n3[n3L - 1][0] - route[len(route) - 1][0]) != 0):
                    for k in range(i + 1, len(route)-1) :
                        n3L = len(n3)
                        if (n3[n3L - 1] != route[k] and n3[n3L - 1] != route[k]):
                            n3.append(route[k])

                        n3L = len(n3)
                        if (abs(n3[n3L - 1][0] - route[len(route) - 1][0]) == 1 or
                                abs(n3[n3L - 1][0] - route[len(route) - 1][0]) == rowInc - 1 or
                                abs(n3[n3L - 1][0] - route[len(route) - 1][0]) == rowInc or
                                abs(n3[n3L - 1][0] - route[len(route) - 1][0]) == rowInc + 1 or
                                abs(n3[n3L - 1][0] - route[len(route) - 1][0]) == 0):
                            break

                if(n3[len(n3) - 1] != route[len(route) - 1]):
                    n3.append(route[len(route) - 1])

                neighbors.append(n3)

        #Move diagonally down
        z4 = route[i-1][0]-rowInc
        if(z4 >= 0 and route[i-1][0] != 0 % rowInc):
            n4.append(zones[z4])

            if(abs(zones[z4][0]-route[i+1][0]) != 1  and abs(zones[z4][0]-route[i+1][0]) != rowInc  and
                abs(zones[z4][0]-route[i+1][0]) != rowInc + 1  and abs(zones[z4][0]-route[i+1][0]) != rowInc - 1):
                n4.append(zones[z4 + rowInc])

                if(abs(zones[z4][0]-route[i+1][0]) > 2*rowInc + 1):
                    n4.append(zones[z4 + 2*rowInc])

            n4L = len(n4)
            if (abs(n4[n4L - 1][0] - route[len(route) - 1][0]) != 1 and
                    abs(n4[n4L - 1][0] - route[len(route) - 1][0]) != rowInc - 1 and
                    abs(n4[n4L - 1][0] - route[len(route) - 1][0]) != rowInc and
                    abs(n4[n4L - 1][0] - route[len(route) - 1][0]) != rowInc + 1 and
                    abs(n4[n4L - 1][0] - route[len(route) - 1][0]) != 0):

                for k in range(i + 1, len(route)-1) :
                    n4L = len(n4)
                    if (n4[n4L - 1] != route[k] and n4[n4L - 1] != route[k]):
                        n4.append(route[k])

                    n4L = len(n4)
                    if (abs(n4[n4L - 1][0] - route[len(route) - 1][0]) == 1 or
                            abs(n4[n4L - 1][0] - route[len(route) - 1][0]) == rowInc - 1 or
                            abs(n4[n4L - 1][0] - route[len(route) - 1][0]) == rowInc or
                            abs(n4[n4L - 1][0] - route[len(route) - 1][0]) == rowInc + 1 or
                            abs(n4[n4L - 1][0] - route[len(route) - 1][0]) == 0):
                        break

            n4L = len(n4)
            if(n4[n4L - 1] != route[len(route) - 1]):
                n4.append(route[len(route) - 1])

            neighbors.append(n4)

        #Move right
        z5 = route[i-1][0]
        if(route[i-1][0] != 0 % rowInc) :
            n5.append(zones[z5])

            if(zones[z5][0]-route[i+1][0] != -1  and abs(zones[z5][0]-route[i+1][0]) != rowInc  and
                abs(zones[z5][0]-route[i+1][0]) != rowInc + 1 and abs(zones[z5][0]-route[i+1][0]) != rowInc - 1):
                if(zones[z5][0]-route[i+1][0] > 0):
                    n5.append(zones[z5 - rowInc])

                else:
                    n5.append(zones[z5 + rowInc])

            n5L = len(n5)
            if (abs(n5[n5L - 1][0] - route[len(route) - 1][0]) != 1 and
                    abs(n5[n5L - 1][0] - route[len(route) - 1][0]) != rowInc - 1 and
                    abs(n5[n5L - 1][0] - route[len(route) - 1][0]) != rowInc and
                    abs(n5[n5L - 1][0] - route[len(route) - 1][0]) != rowInc + 1 and
                    abs(n5[n5L - 1][0] - route[len(route) - 1][0]) != 0):

                for k in range(i + 1, len(route)-1):
                    n5L = len(n5)
                    if (n5[n5L - 1] != route[k] and n5[n5L - 1] != route[k+1]):
                        n5.append(route[k])

                    n5L = len(n5)
                    if (abs(n5[n5L - 1][0] - route[len(route) - 1][0]) == 1 or
                        abs(n5[n5L - 1][0] - route[len(route) - 1][0]) == rowInc - 1 or
                        abs(n5[n5L - 1][0] - route[len(route) - 1][0]) == rowInc or
                        abs(n5[n5L - 1][0] - route[len(route) - 1][0]) == rowInc + 1 or
                        abs(n5[n5L - 1][0] - route[len(route) - 1][0]) == 0):
                        break

            if(n5[n5L - 1][0] != route[len(route) - 1]):
                n5.append(route[len(route) - 1])

            neighbors.append(n5)

    return neighbors

base = [0, -80.143978, 25.769799]
entry = [-80.124404, 25.760130]

LoInc = 20
LatInc = 20

zones = createZones(-80.12878, df['longitude'].max()+.05, df['latitude'].min()-.05, df['latitude'].max()+.000005, 20 ,20)

entryZone = zoneFinder(zones,entry,LoInc)

#Incident Location
point = [-79.88, 25.83]
incidentZone = zoneFinder(zones, point, LoInc)

R = initRoute(zones, base, entryZone, incidentZone, LoInc)


x_curr = initRoute(zones,base,entryZone,incidentZone,LoInc )  #x_curr will hold the current solution
print(x_curr)
x_best = x_curr          #x_best will hold the best solution
f_curr = evaluate(x_curr)   #f_curr will hold the evaluation of the current solution
f_best = f_curr

######################################################################################################
######################################################################################################
#################################Simulated Annealing Logic############################################
######################################################################################################
######################################################################################################
T = 400 #Set initial temperature
while T > 0:
    k = 1
    while k > 0:

        Neighborhood = neighborhood(zones, x_curr, LoInc, LatInc)  # create a list of all neighbors in the neighborhood of x_curr
        L = len(Neighborhood)

        if (L != 0):
            s = ran.randint(0, len(Neighborhood)-1)  # randomly select a neighbor
            if evaluate(Neighborhood[s]) <= f_best:  # Accept if neighbor is better
                x_curr = Neighborhood[s]
                x_best = x_curr

                f_curr = evaluate(Neighborhood[s])
                f_best = f_curr


            else:  # Accept with specified probability if neighbor is worse
                change = f_best - evaluate(Neighborhood[s])
                l = ran.random()


                if l <= (m.e ** (-change / T)):
                    x_curr = Neighborhood[s]
                    f_curr = evaluate(Neighborhood[s])

        k = (k + 1) % 50  # Temperatures are run for 100 iterations

    T = T - 20  # Temperatures are decreased by increments of 5

print(R)
print(x_best)




###### Genetic Algorithm Code #######
##Movement functions for genetic algorithm
def moveUp(routeL, routeR, zones, rowInc, colInc):
        z1 = routeL[len(routeL) - 1][0] + rowInc - 1
        if (z1 < zones[len(zones)-rowInc][0]+1):
            routeL.append(zones[z1])

            if (abs(zones[z1][0] - routeR[0][0]) != rowInc and abs(zones[z1][0] - routeR[0][0]) != rowInc + 1 and
                    abs(zones[z1][0] - routeR[0][0]) != 1 and abs(zones[z1][0] - routeR[0][0]) != rowInc - 1):

                if (abs(zones[z1][0] - routeR[0][0]) == rowInc + 2
                        or abs(zones[z1][0] - routeR[0][0]) == 2):
                    routeL.append(zones[z1 + 1])

                else:
                    routeL.append(zones[z1 - rowInc + 1])

                    if (abs(zones[z1][0] - routeR[0][0]) > 2 * rowInc):
                        routeL.append(zones[z1 - 2 * rowInc + 1])

            L = len(routeL)
            if (abs(routeL[L - 1][0] - routeR[len(routeR)-1][0]) != 1 and
                    abs(routeL[L - 1][0] - routeR[len(routeR)-1][0]) != rowInc - 1 and
                    abs(routeL[L - 1][0] - routeR[len(routeR)-1][0]) != rowInc and
                    abs(routeL[L - 1][0] - routeR[len(routeR)-1][0]) != rowInc + 1 and
                    abs(routeL[L - 1][0] - routeR[len(routeR)-1][0]) != 0):

                routeL.extend(routeR)


            elif (routeL[len(routeL) - 1] != routeR[len(routeR) - 1]):
                routeL.append(routeR[len(routeR) - 1])

            return routeL

        else:
            return routeL.extend(routeR)

def moveDiagUp(routeL, routeR, zones, rowInc, colInc):
    z2 = routeL[len(routeL)-1][0] + rowInc
    if (z2 < rowInc * colInc - 1 and routeL[len(routeL)-1][0] != 0 % rowInc):
        routeL.append(zones[z2])

        if (abs(zones[z2][0] - routeR[0][0]) != rowInc and abs(zones[z2][0] - routeR[0][0]) != 1 and
                abs(zones[z2][0] - routeR[0][0]) != rowInc - 1 and abs(
                    zones[z2][0] - routeR[0][0]) != rowInc + 1):
            routeL.append(zones[z2 - rowInc])

            if (abs(zones[z2][0] - routeR[0][0]) > 2 * rowInc + 1):
                routeL.append(zones[z2 - 2 * rowInc])

        L = len(routeL)
        if (abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != 1 and
                abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != rowInc - 1 and
                abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != rowInc and
                abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != rowInc + 1 and
                abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != 0):

            routeL.extend(routeR)


        elif (routeL[len(routeL) - 1] != routeR[len(routeR) - 1]):
            routeL.append(routeR[len(routeR) - 1])

        return routeL

    else:
        return routeL.extend(routeR)

def moveDown(routeL, routeR, zones, rowInc, colInc):
    z3 = routeL[len(routeL) - 1][0] - rowInc - 1
    if (routeL[len(routeL)-2][0] - routeL[len(routeL) - 1][0] != -rowInc and routeL[len(routeL) - 1][0] != 0 % rowInc and z3 >= 0):

        routeL.append(zones[z3])
        if (abs(zones[z3][0] - routeR[0][0]) != 1 and abs(zones[z3][0] - routeR[0][0]) != rowInc and
                abs(zones[z3][0] - routeR[0][0]) != rowInc - 1 and abs(
                    zones[z3][0] - routeR[0][0]) != rowInc + 1):

            if (abs(zones[z3][0] - routeR[0][0]) != rowInc - 2):
                routeL.append(zones[z3 + 1])

            else:
                routeL.append(zones[z3 + rowInc + 1])
                if (abs(zones[z3][0] - routeR[0][0]) >= 3 * rowInc):
                    routeL.append(zones[z3 + 2 * rowInc + 1])

        L = len(routeL)
        if (abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != 1 and
                    abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != rowInc - 1 and
                    abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != rowInc and
                    abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != rowInc + 1 and
                    abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != 0):

            routeL.extend(routeR)


        elif (routeL[len(routeL) - 1] != routeR[len(routeR) - 1]):
            routeL.append(routeR[len(routeR) - 1])

        return routeL

    else:
        return routeL.extend(routeR)

def moveDiagDown(routeL, routeR, zones, rowInc, colInc):
    z4 = routeL[len(routeL) - 1][0] - rowInc
    if (z4 >= 0 and routeL[len(routeL)-1][0] != 0 % rowInc):
        routeL.append(zones[z4])

        if (abs(zones[z4][0] - routeR[0][0]) != 1 and abs(zones[z4][0] - routeR[0][0]) != rowInc and
                abs(zones[z4][0] - routeR[0][0]) != rowInc + 1 and
                abs(zones[z4][0] - routeR[0][0]) != rowInc - 1):
            routeL.append(zones[z4 + rowInc])

            if (abs(zones[z4][0] - routeR[0][0]) > 2 * rowInc + 1):
                routeL.append(zones[z4 + 2 * rowInc])

        L = len(routeL)
        if (abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != 1 and
                abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != rowInc - 1 and
                abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != rowInc and
                abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != rowInc + 1 and
                abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != 0):

                routeL.extend(routeR)


        elif (routeL[len(routeL) - 1] != routeR[len(routeR) - 1]):
            routeL.append(routeR[len(routeR) - 1])

        return routeL

    else:
        return routeL.extend(routeR)

def moveRight(routeL, routeR, zones, rowInc, colInc):
    z5 = routeL[len(routeL)-1][0]
    if (routeL[len(routeL) - 1][0] != 0 % rowInc):
        routeL.append(zones[z5])

        if (zones[z5][0] - routeR[0][0] != -1 and abs(zones[z5][0] - routeR[0][0]) != rowInc and
                abs(zones[z5][0] - routeR[0][0]) != rowInc + 1 and
                abs(zones[z5][0] - routeR[0][0]) != rowInc - 1):

            if (zones[z5][0] - routeR[0][0] > 0):
                routeL.append(zones[z5 - rowInc])

            else:
                routeL.append(zones[z5 + rowInc])

        L = len(routeL)
        if (abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != 1 and
                abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != rowInc - 1 and
                abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != rowInc and
                abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != rowInc + 1 and
                abs(routeL[L - 1][0] - routeR[len(routeR) - 1][0]) != 0):

            routeL.extend(routeR)


        elif (routeL[len(routeL) - 1] != routeR[len(routeR) - 1]):
            routeL.append(routeR[len(routeR) - 1])

        return routeL

    else:
        return routeL.extend(routeR)



def crossover(route1, route2, zones, rowInc, colInc):

    child1 = route1
    child2 = route2

    if(len(route1) < len(route2)):
        L = len(route1)
    else:
        L = len(route2)

    crossovers = L//4
    if(crossovers == 0):
        crossovers = 1



    crossGenes = []
    for i in range(0, crossovers):
        geneNum = ran.randint(2,L-2)
        crossGenes.append(geneNum)

    crossGenes.sort(reverse=True)

    print(crossGenes)



    for gene in crossGenes:
        Left1 = []
        Left2 = []

        Right1 = []
        Right2 = []

        move1 = route1[gene-1][0] - route1[gene][0]
        move2 = route2[gene-1][0] - route2[gene][0]

        for i in range(0, gene):
            Left1.append(child1[i])
            Left2.append(child2[i])

        for i in range(gene+1, len(child1)):
            Right1.append(child1[i])

        for i in range(gene+1, len(child2)):
            Right2.append(child2[i])

        if (move2 == -rowInc):
            child1 = moveUp(Left1, Right1, zones, rowInc, colInc)

        elif (move2 == -rowInc - 1):
            child1 = moveDiagUp(Left1, Right1, zones, rowInc, colInc)

        elif (move2 == rowInc):
            child1 = moveDown(Left1, Right1, zones, rowInc, colInc)

        elif (move2 == rowInc - 1):
            child1 = moveDiagDown(Left1, Right1, zones, rowInc, colInc)

        else:
            child1 = moveRight(Left1, Right1, zones, rowInc, colInc)



        if (move1 == -rowInc):
            child2 = moveUp(Left2, Right2, zones, rowInc, colInc)

        elif (move1 == -rowInc - 1):
            child2 = moveDiagUp(Left2, Right2, zones, rowInc, colInc)

        elif (move1 == rowInc):
            child2 = moveDown(Left2, Right2, zones, rowInc, colInc)

        elif (move1 == rowInc - 1):
            child2 = moveDiagDown(Left2, Right2, zones, rowInc, colInc)

        else:
            child2 = moveRight(Left2, Right2, zones, rowInc, colInc)



    return [child1, child2]

def mutation(route, zones, rowInc, colInc):
    L = len(route)
    geneMut = ran.randint(2, L - 2)

    Left = []
    Right = []

    for i in range(0, geneMut):
        Left.append(route[i])

    for i in range(geneMut+1, len(route)):
        Right.append(route[i])

    if(geneMut > rowInc*(colInc-1)-1):
        route = moveDiagDown(Left, Right, zones, rowInc, colInc)

    elif(geneMut <= rowInc):
        route = moveDiagUp(Left, Right, zones, rowInc, colInc)

    elif(route[geneMut][0] != 0%rowInc):
        p = ran.random()
        if(p < 0.5):
            route = moveDiagDown(Left, Right, zones, rowInc, colInc)

        else:
            route = moveDiagUp(Left, Right, zones, rowInc, colInc)

    return route



def initPop(zones, base, entryZone, incidentZone, rowInc, colInc, size):
    population = []
    for s in range(0, size):
        population.append([1])

    for i in range(0, size):
        population[i] = []
        population[i].append(base)
        population[i].append(entryZone)

        while(population[i][len(population[i])-1][0] != incidentZone[0]):
            p = ran.random()
            z = population[i][len(population[i])-1][0]-1

            if (zones[z][1] == incidentZone[1]):
                if(zones[z][3] < incidentZone[3]):
                    population[i].append(zones[z + rowInc])

                elif(zones[z][3] > incidentZone[3]):
                    population[i].append(zones[z-rowInc])

            else:
                if(z > rowInc*(colInc-1)):
                    if(p <= 0.333):
                        population[i].append(zones[z-rowInc])
                    elif(p > 0.333 and p <= 0.666):
                        population[i].append(zones[z-rowInc+1])
                    else:
                        population[i].append(zones[z+1])

                elif(z < rowInc):
                    if (p <= 0.333):
                        population[i].append(zones[z + rowInc])
                    elif (p > 0.333 and p <= 0.666):
                        population[i].append(zones[z + rowInc + 1])
                    else:
                        population[i].append(zones[z + 1])

                else:
                    if (p <= 0.2):
                        population[i].append(zones[z + rowInc])
                    elif (p > 0.2 and p <= 0.4):
                        population[i].append(zones[z + rowInc + 1])
                    elif(p > 0.4 and p <= 0.6):
                        population[i].append(zones[z + 1])
                    elif(p > 0.6 and p <= 0.8):
                        population[i].append(zones[z-rowInc])
                    else:
                        population[i].append(zones[z-rowInc+1])

            if(abs(population[i][len(population[i])-1][0] - incidentZone[0]) == 1 or
                abs(population[i][len(population[i])-1][0] - incidentZone[0]) == rowInc - 1 or
                abs(population[i][len(population[i])-1][0] - incidentZone[0]) == rowInc or
                abs(population[i][len(population[i])-1][0] - incidentZone[0]) == rowInc + 1 or
                abs(population[i][len(population[i])-1][0] - incidentZone[0]) == 0):

                population[i].append(incidentZone)


    return population

Population = []


##############################################################################################
##############################################################################################
#################################Genetic Algorithm Logic######################################
##############################################################################################
##############################################################################################

Generations = 10
Population = initPop(zones, base, entryZone, incidentZone, 20, 20, 3)
print(Population)
popLimit = 10

for i in range(0, Generations):
    ##Crossover rate 25% per generation
    popSize = len(Population)
    crossTimes = popSize // 4
    if (crossTimes == 0):
        crossTimes = 1

    for i in range(0, crossTimes):
        ##Select solutions to cross
        s1 = ran.randint(0, popSize-1)
        s2 = ran.randint(0, popSize-1)

        ##Cross them
        children = crossover(Population[s1], Population[s2], zones, 20, 20)
        Population.extend(children)


    mutations = popSize//10
    if(mutations == 0):
        mutations = 1

    for j in range(0, mutations):
        ##Select members to mutate
        M = ran.randint(0, len(Population) - 1)
        ##Mutate
        Population[M] = mutation(Population[M], zones, 20, 20)

    ##Order by eval
    Population.sort(key=evaluate)

    ##Limit population
    if(len(Population) > popLimit):
        redPop = []
        for k in range(0, popLimit):
            redPop.append(Population[k])

        Population = redPop

    print(Population[0])

print(Population[0:3])


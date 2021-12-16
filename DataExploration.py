import pandas as pd
import datetime as dt
from sklearn import linear_model

df = pd.read_excel (r'ProjectData1.xlsx')
df['zone'] = ''


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

zone = []



#zones = createZones(df['longitude'].min()-.05, df['longitude'].max()+.05, df['latitude'].min()-.05, df['latitude'].max()+.05, 10 ,10)

zones = createZones(-80.12878, df['longitude'].max()+.05, df['latitude'].min()-.05, df['latitude'].max()+.000005, 20 ,20)

zonesTest = createZones(-80.12878, df['longitude'].max()+.05, df['latitude'].min()-.05, df['latitude'].max()+.000005, 20 ,20)

for i in range(0, len(df['longitude'])):
    #zone.append(zoneFinder(zones, [df1['longitude'][i], df1['latitude'][i]], 10)[0])
    z = zoneFinder(zones, [df['longitude'][i], df['latitude'][i]], 20)
    df.loc[i, 'zone'] = z[0]

df['Time'] = pd.to_datetime(df['BaseDateTime']).dt.time
df['Date'] = pd.to_datetime(df['BaseDateTime']).dt.date

df1 = df[['BaseDateTime','longitude', 'latitude', 'zone']]
df1['Time'] = pd.to_datetime(df1['BaseDateTime']).dt.time
df1['Date'] = pd.to_datetime(df1['BaseDateTime']).dt.date
df1 = df1[df1['longitude']> -80.12878]

time = dt.datetime(2021, 12, 2, 14, 20)

date = []
zone = []
zoneLong = []
zoneLat = []
count = []

for i in range(1, 32):
    for j in range(0, len(zones)):
        day = dt.date(2009, 1, i)
        date.append(day)
        zone.append(zones[j][0])
        zoneLong.append((zones[j][1] + zones[j][2])/2)
        zoneLat.append((zones[j][3] + zones[j][4]) / 2)
        count.append('')

D = [date, zone, zoneLong, zoneLat, count]
train = pd.DataFrame(data = D)
train = train.transpose()
train.columns = ["Date", "Zone", "Longitude", "Latitude", "Vessels"]



time_change =dt.timedelta(minutes=15)
max_time = time + time_change
min_time = time - time_change


trainData = df1[df1["Time"].between(min_time.time(), max_time.time())]
trainData.head()



def vesselCounter(data, date, zone):
    counter = 0
    t = data[data["Date"] == date]
    t = t[t["zone"] == zone]
    counter = len(t)
    return counter

for i in range(0, len(train['Zone'])):
    train.loc[i, 'Vessels'] = vesselCounter(trainData, train.loc[i, 'Date'], train.loc[i, 'Zone'])


X = train[["Longitude", "Latitude"]]
Y = train[["Vessels"]]


testLong = []
testLat = []

for j in range(0,len(zones)):
    testLong.append((zones[j][1] + zones[j][2])/2)
    testLat.append((zones[j][3] + zones[j][4]) / 2)

d = [testLong, testLat]
test = pd.DataFrame(data = d)
test = test.transpose()
test.columns = ["Longitude", "Latitude"]
test.head()


regr = linear_model.LinearRegression()
regr.fit(X, Y)

predictedZones = regr.predict(test)

predictedZones

yHat = regr.predict(X)

# importing r2_score module
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
# predicting the accuracy score
score=r2_score(Y,yHat)
print("r2 socre is ",score)



Busy = []
for i in range(0, len(Y)):
    if(Y["Vessels"][i] > .5):
        Busy.append("Yes")
    else:
        Busy.append("No")



from sklearn.neighbors import NearestCentroid
import numpy as np
clf = NearestCentroid()
clf.fit(X, Busy)
clf.score(X, Busy)

predZones = clf.predict(test)

hotZones = []
for i in range(0, len(predictedZones)):
    if(predZones[i] == 'Yes'):
        hotZones.append(zones[i][0])

hotZones

import matplotlib.pyplot as plt
from PIL import Image

img = Image.open("Miami.JPG")


##Graph for instance
fig, ax = plt.subplots()
ax.imshow(img)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.scatter((2000*trainData['longitude']+160630), (-2000*trainData['latitude']+51965), s = .005, color = "Black")
ax.set_title("Traffic History for 2:20 pm")
plt.show()

plt.hist(df1['zone'], bins=100)
plt.hist(df1['zone']%10, bins = 10)

times = []
for i in range(0, len(df1['Date'])):
    times.append((df['BaseDateTime'][i]-dt.datetime(df['Date'][i].year, df['Date'][i].month,df['Date'][i].day)).total_seconds()/3600)

fig, ax = plt.subplots()
ax.hist(times, bins = 24, rwidth = 0.9)
ax.set_title("Time Histogram")
plt.xlabel('Hour in the Day')
plt.ylabel('Frequency')
plt.show()


fig, ax = plt.subplots()
ax.imshow(img)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.scatter((2000*df['longitude']+160630), (-2000*df['latitude']+51965), s = .005, color = "Black")
plt.show()

TestX = []
TestY = []

for i in range(0, len(zones)):
    TestX.append(2000*(zones[i][1]+zones[i][2])/2 + 160630)
    TestY.append(-2000*(zones[i][3]+zones[i][4])/2 + 51965)

hotLong = []
hotLat = []

for i in hotZones:
    hotLong.append(2000*(zones[i-1][1] + zones[i-1][2])/2 + 160630)
    hotLat.append(-2000*(zones[i-1][3] + zones[i-1][4]) / 2 + 51965)


fig, ax = plt.subplots()
ax.imshow(img)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.scatter(TestX, TestY, s = 1, color = "Black")
ax.set_title("Zoned Area")
plt.show()

initGen1 = [201, 202, 223, 224, 244, 245, 225, 226, 227, 207, 188, 169, 190, 191, 212, 192, 213, 193, 214, 234, 254,
            274, 294, 314, 334]
iG1Long = []
iG1Lat = []

for i in initGen1:
    iG1Long.append(2000*(zones[i-1][1] + zones[i-1][2])/2 + 160630)
    iG1Lat.append(-2000*(zones[i-1][3] + zones[i-1][4]) / 2 + 51965)


initGen2 = [201, 202, 182, 183, 164, 144, 145, 165, 166, 186, 187, 207, 188, 168, 149, 150, 170, 190, 211, 191, 192,
            173, 174, 194, 214, 234, 254, 274, 294, 314, 334]
iG2Long = []
iG2Lat = []

for i in initGen2:
    iG2Long.append(2000*(zones[i-1][1] + zones[i-1][2])/2 + 160630)
    iG2Lat.append(-2000*(zones[i-1][3] + zones[i-1][4]) / 2 + 51965)


initGen3 = [201, 181, 162, 163, 143, 163, 183, 164, 184, 165, 186, 167, 187, 207, 187, 168, 148, 128, 148, 168, 189,
            170, 151, 172, 153, 173, 153, 133, 154, 174, 194, 214, 234, 254, 274, 294, 314, 334]
iG3Long = []
iG3Lat = []

for i in initGen3:
    iG3Long.append(2000*(zones[i-1][1] + zones[i-1][2])/2 + 160630)
    iG3Lat.append(-2000*(zones[i-1][3] + zones[i-1][4]) / 2 + 51965)

fig, ax = plt.subplots()
ax.imshow(img)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.scatter(TestX, TestY, s = 1, color = "Black")
ax.scatter(hotLong, hotLat, s = 5, color = "Red")
ax.plot(iG1Long, iG1Lat)
ax.plot(iG2Long, iG2Lat)
ax.plot(iG3Long, iG3Lat)
plt.show()

finGen1 = [201, 202, 203, 224, 245, 226, 227, 248, 249, 270, 271, 292, 273, 294, 314, 334]

fG1Long = []
fG1Lat = []

for i in finGen1:
    fG1Long.append(2000*(zones[i-1][1] + zones[i-1][2])/2 + 160630)
    fG1Lat.append(-2000*(zones[i-1][3] + zones[i-1][4]) / 2 + 51965)


finGen2 = [201, 202, 203, 224, 245, 226, 227, 228, 229, 230, 251, 272, 292, 313, 333, 334]
fG2Long = []
fG2Lat = []

for i in finGen2:
    fG2Long.append(2000*(zones[i-1][1] + zones[i-1][2])/2 + 160630)
    fG2Lat.append(-2000*(zones[i-1][3] + zones[i-1][4]) / 2 + 51965)


finGen3 = [201, 202, 203, 224, 245, 226, 227, 228, 229, 230, 251, 271, 292, 313, 334]
fG3Long = []
fG3Lat = []

for i in finGen3:
    fG3Long.append(2000*(zones[i-1][1] + zones[i-1][2])/2 + 160630)
    fG3Lat.append(-2000*(zones[i-1][3] + zones[i-1][4]) / 2 + 51965)

fig, ax = plt.subplots()
ax.imshow(img)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.scatter(TestX, TestY, s = 1, color = "Black")
ax.scatter(hotLong, hotLat, s = 5, color = "Red")
ax.plot(fG1Long, fG1Lat)
ax.plot(fG2Long, fG2Lat)
ax.plot(fG3Long, fG3Lat)
plt.show()

initSim = [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 234, 254, 274, 294, 314, 334]

iSZones = []
for i in finGen3:
    iSZones.append(zones[i-1])

iSimLong = []
iSimLat = []

for i in initSim:
    iSimLong.append(2000*(zones[i-1][1] + zones[i-1][2])/2 + 160630)
    iSimLat.append(-2000*(zones[i-1][3] + zones[i-1][4]) / 2 + 51965)


midSim = [201, 202, 203, 204, 205, 206, 207, 208, 189, 190, 210, 211, 212, 233, 254, 274, 294, 314, 334]
mSimLong = []
mSimLat = []

for i in midSim:
    mSimLong.append(2000*(zones[i-1][1] + zones[i-1][2])/2 + 160630)
    mSimLat.append(-2000*(zones[i-1][3] + zones[i-1][4]) / 2 + 51965)


finalSim = [201, 202, 203, 204, 205, 206, 207, 208, 189, 210, 231, 251, 272, 293, 313, 334]
fSimLong = []
fSimLat = []

for i in finalSim:
    fSimLong.append(2000*(zones[i-1][1] + zones[i-1][2])/2 + 160630)
    fSimLat.append(-2000*(zones[i-1][3] + zones[i-1][4]) / 2 + 51965)

fig, ax = plt.subplots()
ax.imshow(img)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.scatter(TestX, TestY, s = 1, color = "Black")
ax.scatter(hotLong, hotLat, s = 5, color = "Red")
ax.plot(iSimLong, iSimLat)
ax.plot(mSimLong, mSimLat)
ax.plot(fSimLong, fSimLat)
plt.show()


fig, ax = plt.subplots()
ax.imshow(img)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.scatter(TestX, TestY, s = 1, color = "Black")
ax.scatter(hotLong, hotLat, s = 5, color = "Red")
ax.plot(fSimLong, fSimLat)
ax.plot(fG3Long, fG3Lat)
plt.show()

count = 0
for i in finGen3:
    for j in hotZones:
        if(i == j):
            count = count + 1
count

Gen = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Moves = [31.33, 29.67, 28.3, 26.67, 20.67, 19, 18.67, 16.33, 16, 15.67]
Eval = [1163.096, 1160.172, 1156.574, 1154.747, 1142.208, 1140.753, 1138.606, 1133.436, 1131.975, 1130.102]

fig, ax = plt.subplots()
ax.set_title("Change in Number of Moves")
plt.xlabel('Generation')
plt.ylabel('Moves')
ax.plot(Gen, Moves)
plt.show()

fig, ax = plt.subplots()
ax.set_title("Change in Evaluation")
plt.xlabel('Generation')
plt.ylabel('Evaluation')
ax.plot(Gen, Eval)
plt.show()
import json
import requests
import googlemaps
from datetime import datetime

#mykey
myApi = "AIzaSyAE48EgrotEWr6H3-60SGekPxH7jXUv9Rw"
gmaps = googlemaps.Client(key= myApi)


# Geocoding an address
#using an address....

# reference code.
#
# umbc = gmaps.geocode('1000 Hilltop Circle, Balitmore, MD')
# ledo = gmaps.geocode("4636 Wilkens Ave, Baltimore, MD")
# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
# Request directions via public transit

#
# now = datetime.now()
# directions_result = gmaps.directions("1000 Hilltop Circle, Balitmore MD",
#                                      "4636 Milkens Ave, Baltimore, MD",
#                                      mode="transit",
#                                      departure_time=now)


#List of headquarters.
hq = ["1000 Hilltop Circle, Balitmore MD", "4636 Milkens Ave, Baltimore, MD", "800 S Rolling Rd, Catonsville, MD"]

#list of emergencies.
missions = {}
emergencies = {}
#unique identifer
emegNum = 0
missNum = 0

def createLink(orgin, dest):
    #convert the location into a lat and long string.
    orgin = gmaps.geocode(orgin)
    try:
        orgLoc = str(orgin[0]["geometry"]["location"]["lat"]) + "," + str(orgin[0]["geometry"]["location"]["lng"])
        dest = gmaps.geocode(dest)
        destLoc = str(dest[0]["geometry"]["location"]["lat"]) + "," + str(dest[0]["geometry"]["location"]["lng"])
    except:
        return "invalid address"

    #creating links
    #Link from org to dest in json format
    myLink = "https://maps.googleapis.com/maps/api/directions/json?origin="+ orgLoc + "&destination=" + destLoc + "&key=" + myApi

    #google map links for user to have visualization of the route.
    orgtoDest = "https://www.google.com/maps/dir/?api=1&origin=" + orgLoc + "&destination=" + destLoc + "&travelmode=driving"
    userToDest = "https://www.google.com/maps/search/?api=1&query=" + destLoc

    return myLink, orgtoDest , userToDest , orgLoc , destLoc

def getRouteData(link):

    response = requests.get(link)
    myData = json.loads(response.text)
    return myData

def routeDur(rData):
    duration = rData["routes"][0]["legs"][0]["duration"]["text"]
    return duration

def getDuration(orgin, dest):
    myLink = createLink(orgin, dest)
    if myLink == "invalid address":
        return "invalid address"
    return routeDur(getRouteData(myLink[0])) , myLink[1], myLink[2] , myLink[3], myLink[4]


#finding the closest headquarter to the destimation
def closeHQ(dest):
    #storing the clostest location and its information.
    bestRoute = hq[0]
    bestTime = -1
    bestData = ""

    #finding the closest location
    for x in hq:
        routeData = getDuration(x , dest)
        if routeData == "invalid address":
            return "invalid address"
        else:
            tempRoute = routeData[0]
            # print(x, tempRoute)
            if bestTime == -1:
                bestRoute = x
                bestTime = tempRoute
                bestData = routeData

            elif tempRoute < bestTime:
                bestRoute = x
                bestTime = tempRoute
                bestData = routeData
    return [bestRoute , bestTime, bestData[1] , bestData[2] , bestData[3], bestData[4]]


#using the given destination, we return the closest headquarter, the estimated time, and a google map link for the responder to use.
def getBestRoute(dest , id):
    routeData = closeHQ(dest)
    #tuple with lat, lng, time
    if routeData == "invalid address":
        return "invalid address"
    return {"orgin" : routeData[4], "dest" : routeData[5] , "time" : routeData[1], "rLink" : routeData[2] , "uLink" : routeData[3]}
    # print(emergencies)
    # print("Send to Headquarters : " , routeData[0])
    # print("Estimated Time : " , routeData[1])
    # print("Direction List Link : " , routeData[2])
    # print("User to Dest Link : " , routeData[3])


#get emergency, input destination, description of emergency, category, and the priority ranking.
def getEmergency(dest , description, category , priority):
    global emegNum
    global missNum

    myEmeg = getBestRoute(dest, emegNum)


    if myEmeg == "invalid address":
        return "invalid address"


    myEmeg["Description"] = description
    myEmeg["Category"] = category
    myEmeg["Priority"] = priority
    myEmeg["Status"] = "created"

    org = myEmeg["orgin"]
    org = list(map(float, org.split(",")))  # convert into a list of int, instead of string.

    storeMission = {}
    removeEm = []

    tSize = .05

    for x in emergencies:

        temp = emergencies[x]["orgin"]
        temp = list(map(float, temp.split(","))) #convert into a list of int, instead of string.

        if (bool(storeMission)):
            tSize = storeMission["size"]


        if (temp[0] - org[0] <= tSize and temp[1] - org[1] <= .05 and myEmeg["Category"] == emergencies[x]["Category"]):
            #create an emergency...
            removeEm.append(x)
            tempOrg = [(temp[0]+org[0])/2 , (temp[1] + org[1])/2]
            if (not bool(storeMission)):
                storeMission = {"orgin" : tempOrg , "Category" : category,"Description" : [description, emergencies[x]["Description"]] ,
                                "size" : .05, "locations" : [tempOrg , org], "total" : 2,
                                "rLinks" : [emergencies[x]["rLink"],myEmeg["rLink"]] , "uLinks" : [emergencies[x]["uLink"],myEmeg["uLink"]]}

            else:
                storeMission["size"] *= 1.25
                storeMission["locations"].append(tempOrg)
                storeMission["Description"] = emergencies[x]["Description"]
                storeMission["uLinks"].append(emergencies[x]["uLinks"])
                storeMission["rLinks"].append(emergencies[x]["rLinks"])
                storeMission["total"] += 1


    for x in removeEm:
        emergencies.pop(x, None)

    if (bool(storeMission)):
        #if there is an emergency
        missions[missNum] = storeMission
    else:
        #if there is no emegerncy
        emergencies[emegNum] = myEmeg

    return myEmeg["uLink"]




#Address, description, category, priority.

#return link or invalid address.
print(getEmergency("5520 Research Park Dr, Catonsville, MD 21228" , "House fire" , "Fire" , 5))

print(getEmergency("5525 Research Park Dr, Catonsville, MD 21228" , "House fire" , "Fire" , 5))

print(getEmergency(" " , "test" , "Fire" , 5))


#
# print("Missions")
# for x in missions:
#     print(missions[x])
#     for y in range(missions[x]["total"]):
#         print("\t" , missions[x]["locations"][y])
#         print("\t" , missions[x]["rLinks"][y])
#         print("\t" , missions[x]["uLinks"][y])
#         print("\t" , missions[x]["Description"][y])
#     print("----------")
#
# print("Emergencies")
# for x in emergencies:
#     print(emergencies[x])
#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Arpan Ojha arojha
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
import math
def successor(fringe,graph,gps_data,goal):
    seg=fringe[4]
    delivery_time=fringe[6]
    next_cities=graph.get(fringe[0])
    if next_cities is None:
        return None
    next_fringe=[]
    dist=fringe[1]
    path=fringe[3]
    for i in next_cities:
        path=fringe[3]
        d=i[1]
        seg1=seg
        t_t=fringe[5]
        prob=0
        if int(i[2])>=50: 
            prob=math.tanh(int(d)/1000)
        q=int(i[1])/int(i[2])
        w=delivery_time
        s=w+q+(prob*(q+w)*2)
        t_t+=int(i[1])/int(i[2])
        if path is not None:
            next_fringe.append([i[0],(int(d)+int(dist)),float(heuristic(i[0],goal,gps_data,fringe[2])),fringe[3]+[(i[0],i[3]+" for "+i[1]+" miles")],seg+1,t_t,s])
        else:
            next_fringe.append([i[0],(int(d)+int(dist)),float(heuristic(i[0],goal,gps_data,fringe[2])),[(i[0],i[3]+" for "+i[1]+" miles")],seg+1,t_t,s])
    return next_fringe

import math
def distance_x_y(city_x, city_y,gps_data):
    lat1,long1 = gps_data[city_x][0], gps_data[city_x][1]
    lat2,long2 = gps_data[city_y][0], gps_data[city_y][1]
    return math.sqrt((lat1 - lat2)**2 + (long1 - long2)**2)

def heuristic(start, goal, gps_data,prev_val):
    next_gps=gps_data.get(start)
    if next_gps is None:
        return prev_val
    return distance_x_y(start, goal,gps_data)


def city_gps_from_file():
    gps_data = {}
    with open('city-gps.txt', 'r') as f:
        for line in f.readlines():
            each_city = line.split()
            city = each_city[0]
            latitude = float(each_city[1])
            longitude = float(each_city[2])
            gps_data[city] = (latitude, longitude)
    return gps_data

def pick_lowest_heurestic(fringe):
    low_i=float(fringe[0][2])
    lowest_i=0
    for i in range(len(fringe)):
        if fringe[i][2]<low_i:
            lowest_i=i
            low_i=fringe[i][2]
    return lowest_i

def pick_speed_limit(fringe,graph_city):
    time_taken=int(graph_city[fringe[0][0]][0][1])/int(graph_city[fringe[0][0]][0][2])
    lowest_i=0
    for i in range(len(fringe)):
        next_list=graph_city[fringe[i][0]]
        for j in next_list:
            t_t=int(j[1])/int(j[2])
            print(fringe[i][0],j[1],j[2],j[0],t_t)
            if t_t<time_taken:
                time_taken=t_t
                lowest_i=i
    return lowest_i,t_t

        
def pick_delivery_distance(fringe):
    low_dist=fringe[0][6]
    low_i=0
    for i in range(len(fringe)):
        if fringe[i][6]<low_dist:
            low_dist=fringe[i][6]
            low_i=i
    return low_i

def pick_shortest_distance(fringe):
    low_i=float(fringe[0][2])+fringe[0][1]
    lowest_i=0
    for i in range(len(fringe)):
        if fringe[i][2]+fringe[i][1]<low_i:
            lowest_i=i
            low_i=fringe[i][2]+fringe[i][1]
    return lowest_i


def pick_less_segments(fringe):
    les_seg=fringe[0][4]
    low_i=0
    for i in range(len(fringe)):
        if les_seg>fringe[i][4]:
            low_i=i
            les_seg=fringe[i][4]
    return low_i

def pick_less_time(fringe):
    les_seg=fringe[0][5]
    low_i=0
    for i in range(len(fringe)):
        if les_seg>fringe[i][5]:
            low_i=i
            les_seg=fringe[i][5]
    return low_i


def get_route(start, end, cost):
    graph_city={}
    file1=open("road-segments.txt","r", encoding='utf-8')
    for line in file1:
        key,v1,v2,v3,v4=line.split()
        if key in graph_city:
            graph_city[key].append([v1,v2,v3,v4])
        else:
            graph_city[key]=[[v1,v2,v3,v4]]
        if v1 in graph_city:
            graph_city[v1].append([key,v2,v3,v4])
        else:
            graph_city[v1]=[[key,v2,v3,v4]]
    gps_data=city_gps_from_file()

    next_city=""
    begin_city=start
    # position, segment length, heurestic= segment length+goal
    path=[] 
    fringe=[[start,0,float(heuristic(start,end,gps_data,0)),path,0,0,0]]
    visited=[]     
    time_taken=0
    return_value = {"total-segments" : 0,
            "total-miles" : 0.0,
            "total-hours" : 0.0,
            "total-delivery-hours" : 0.0,
            "route-taken" : []}
    while True:
        if fringe is None:
            return False
        t_t=0

        if cost =="distance":
            pop_move=pick_shortest_distance(fringe)
        elif cost=="segments":
            pop_move=pick_less_segments(fringe)    
        elif cost=="time":
            pop_move=pick_less_time(fringe)       
        elif cost=="delivery":
            pop_move=pick_delivery_distance(fringe)
        time_taken+=t_t
        next_move=fringe.pop(pop_move)
        if next_move[0] in visited:
            continue
        if next_move[0] not in visited:
            visited.append(next_move[0])

        list_of_next_cities=successor(next_move,graph_city,gps_data,end)
        if list_of_next_cities is None:
            continue

        for options in list_of_next_cities:

            if options[0]==end:

                return_value["total-segments"]=int(options[4])
                return_value["total-miles"]=float(options[1])
                return_value["total-hours"]=float(options[5])
                return_value["route-taken"]=options[3]
                return_value["total-delivery-hours"]=float(options[6])
                return return_value
            if options[0] in visited:
                continue

            fringe.append(options)





# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)
    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])

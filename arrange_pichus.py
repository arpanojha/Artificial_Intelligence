#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Arpan Ojha arojha
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' ]

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k

#find all pichus in a given map and return a list of their coordinates
def find_all_pichu(map1):
    return_pos=[]
    for i in range(len(map1)):
        for j in range(len(map1[0])):
            if map1[i][j] == 'p':
                return_pos.append((i,j))
    return return_pos

#check row for valid position
def left_right_check(map1,j):
    r=j[0]
    c=j[1]
    for i in range(c+1,len(map1[0])):
        if i>=len(map1[0]):
            break
        if map1[r][i]=='p':
            return False
        if map1[r][i]=='X' or map1[r][i]=='@':
            break
    for i in range(c-1,-1,-1):
        if c==-1:
            break
        if map1[r][i]=='p':
            return False
        if map1[r][i]=='X' or map1[r][i]=="@":
            return True
    return True

#check column for valid position
def up_down_check(map1,j):
    r=j[0]
    c=j[1]
    for i in range(r+1,len(map1)):
        if i>=len(map1):
            break
        if map1[i][c]=='p':
            return False
        if map1[i][c]=='X' or map1[i][c]=="@":
            break
    for i in range(r-1,-1,-1):
        if i==-1:
            break
        if map1[i][c]=='p':
            return False
        if map1[i][c]=='X' or map1[i][c]=='@':
            return True
    return True

#check is a given row and column number isvalid in map
def check_r_c_validity(r,c,map1):
    r1=len(map1)
    c1=len(map1[0])
    if r<0 or r>=r1 or c<0 or c>=c1:
        return False
    return True

#check diagonal for valid position
def diagonal_check(map1,j):
    r=j[0]
    c=j[1]
    for i, j in zip(range(r-1,-1,-1),range(c-1,-1,-1)):
        if check_r_c_validity(i,j,map1) is True:
            if map1[i][j]=='p':
                return False
            if map1[i][j]=='X' or map1[i][j]=='@':
                break
    for i, j in zip(range(r-1,-1,-1),range(c+1,len(map1[0]),1)):
        if check_r_c_validity(i,j,map1) is True:
            if map1[i][j]=='p':
                return False
            if map1[i][j]=='X' or map1[i][j]=='@':
                break
    for i, j in zip(range(r+1,len(map1),1),range(c-1,-1,-1)):
        if check_r_c_validity(i,j,map1) is True:
            if map1[i][j]=='p':
                return False
            if map1[i][j]=='X' or map1[i][j]=='@':
                break
    for i,j in zip(range(r+1,len(map1),1),range(c+1,len(map1[0]),1)):
        if check_r_c_validity(i,j,map1) is True:
            if map1[i][j]=='p':
                return False
            if map1[i][j]=='X' or map1[i][j]=='@':
                return True

    return True

#check validity of successor map
def check_validity(map1):
    all_k=find_all_pichu(map1)
#    print("Found pichus ",all_k)
    for j in all_k:
        if left_right_check(map1,j) is False:
            return False
        if up_down_check(map1,j) is False:
            return False
        if diagonal_check(map1,j) is False:
            return False
    return True
# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
#Depth first search applied via Search algorithm number 2
#Check validity of successor to quickly reject
#
def solve(initial_house_map,k):
    if is_goal(initial_house_map,k):
        return (initial_house_map,True)
    fringe = [initial_house_map]
    while len(fringe) > 0:
        if fringe is None:
            return False
        new_one=fringe.pop()
        if check_validity(new_one) is False:
            continue
        if is_goal(new_one,k):
            return(new_one,True)
        for new_house_map in successors( new_one ):
          #  if is_goal(new_house_map,k):
          #      return(new_house_map,True)
            fringe.append(new_house_map)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    if solution is None:
        print("False")
    else:
        print (printable_house_map(solution[0]) if solution[1] else "False")


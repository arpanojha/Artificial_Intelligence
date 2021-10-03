# Artificial_Intelligence

Arrange pichus solution  
In the map,  
Pichu is your pet represented by p   
You are at '@'   
Wall are represented by 'X'  
Solution arranges a given number of pichus such that no two pichus face each other diagonally,in a row or column.  

Example run :  python3 arrange_pichus.py map1.txt 6  

Starting from initial house map:  
....XXX  
.XXX...  
....X..  
.X.X...  
.X.X.X.  
pX...X@  

Looking for solution...  

Here's what we found:  
....XXX  
.XXX...  
...pXp.  
.X.X...  
.XpX.Xp  
pX..pX@  



#Misere Tic tac toe  
Skeleton code credits to CSC551 course  
In this game the person who makes one successful row or column or diagonal in X will lose the game   
In the AI enabled game we have implemented minimax algorithm for AI to think 7 moves ahead and determine if they can win or not  
if they find no such possibility they will simply play a random move untill they think they can win.   
Its fun and once computer has determined they can win they will . Try beating it :)  

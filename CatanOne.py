prob = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for die1 in range(1, 7) :
	for die2 in range(1,7):
		sum = die1 + die2
		prob[sum] += 1 
print(str(prob))

NONE = 0
WHEAT = 1
WOOD = 2
SHEEP = 3
CLAY = 4
STONE = 5

joints = [
[ [ ], [    ], [      ], [0       ], [        ], [1       ], [        ], [2       ], [        ], [     ], [  ] ],
[ [ ], [    ], [0     ], [        ], [0,1     ], [        ], [1,2     ], [        ], [2       ], [     ], [  ] ],
[ [ ], [    ], [0,3   ], [        ], [0,1,4   ], [        ], [1,2,5   ], [        ], [2,6     ], [     ], [  ] ],
[ [ ], [3   ], [      ], [0,3,4   ], [        ], [1,4,5   ], [        ], [2,5,6   ], [        ], [6    ], [  ] ],
[ [ ], [3,7 ], [      ], [3,4,8   ], [        ], [4,5,9   ], [        ], [5,6,10  ], [        ], [6,11 ], [  ] ],
[ [7], [    ], [3,7,8 ], [        ], [4,8,9   ], [        ], [5,9,10  ], [        ], [6,10,11 ], [     ], [11] ],
[ [7], [    ], [7,8,12], [        ], [8, 9, 13], [        ], [9,10,14 ], [        ], [10,11,15], [     ], [11] ],
[ [ ], [7,12], [      ], [8,12,13 ], [        ], [9,13,14 ], [        ], [10,14,15], [        ], [11,15], [  ] ],
[ [ ], [12  ], [      ], [12,13,16], [        ], [13,14,17], [        ], [14,15,18], [        ], [15   ], [  ] ],
[ [ ], [    ], [12,16 ], [        ], [13,16,17], [        ], [14,17,18], [        ], [15,18   ], [     ], [  ] ],
[ [ ], [    ], [16    ], [        ], [16,17   ], [        ], [17,18   ], [        ], [18      ], [     ], [  ] ],
[ [ ], [    ], [      ], [16      ], [        ], [17      ], [        ], [18      ], [        ], [     ], [  ] ]
]


class Tile:        
        def __init__(self, value, tileNum, typ):
                tilesPerRow = [3, 4, 5, 4, 3]

                self.tileNumber = tileNum
                self.rowNum = Tile.getRowNum(tileNum)

                # topLeft neighbor, tr neighbor, 
                self.neighborIds = [tileNum - tilesPerRow[self.rowNum], tileNum-tilesPerRow[self.rowNum] + 1,
                                    tileNum - 1, tileNum + 1,   # left neighbor, right n
                                    tileNum + tilesPerRow[self.rowNum], tileNum + tilesPerRow[self.rowNum] + 1] # bln, brn

                self.resource = typ
                self.value = value

        @staticmethod
        def getRowNum(tileNum):
                if tileNum in range(0, 3):
                        return 0
                elif tileNum in range(3, 7):
                        return 1
                elif tileNum in range(7, 12):
                        return 2
                elif tileNum in range(12, 16):
                        return 3
                elif tileNum in range(16, 19):
                        return 4
                else:
                        return -1

        # return the probability of gaining that certain resource from this node. 
        def p(self, res):
                if self.resource == res:
                        return prob[self.value]
                return 0


# These nodes have already been taken
FILTER =   [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def applyFilter(probs, fltr):
    res = []
    for i in range(len(probs)):
        row = []
        for j in range(len(probs[0])):
            if fltr[i][j] == 1:
                row.append(0)
            else:
                row.append(probs[i][j])
        res.append(row)
    return res



class Grid:
        def __init__(self):
                STN = STONE
                WHT = WHEAT
                SHP = SHEEP
                CLY = CLAY
                WOD = WOOD
                NON = NONE

                
                v =  [    8,     3,      6,
                       11,    11,    10,     9,
                     5,    8,      0,     2,    3,
                        12,   5,     4,     10,
                           6,     4,     9]

                
                rs = [         WHT,    CLY,    SHP,
                           WHT,    CLY,    WOD,    WOD,
                        SHP,   CLY,    NON,    WOD,    STN,
                            WHT,   SHP,    STN,    WHT,
                                SHP,   WOD,    STN]
                self.tiles = []
                for i in range(0, 19):
                        self.tiles.append(Tile(v[i], i, rs[i]))


        def getProbabilityFor(self, r):
                t = self.tiles
                s = self

                probs = []
                for line in joints:
                        probsLine = []
                        for joint in line:
                                probsLine.append(self.c(r, joint))
                        probs.append(probsLine)

                return applyFilter(probs, FILTER)
        
        def getTotalProbability(self):
                t = self.tiles
                probs = []
                for line in joints:
                        probsLine = []
                        for joint in line:
                                probsLine.append(self.tot(joint))
                        probs.append(probsLine)

                return applyFilter(probs, FILTER)

                
                
        def c(self, r, elems):
                sum = 0
                for index in elems:
                        sum += self.tiles[index].p(r)
                return sum

        def tot(self, elems):
                sum = 0
                for index in elems:
                        sum += prob[self.tiles[index].value]
                return sum
        
def printMatrix(matrix):
        newMat = ""
        print("     " + str(''.join('%3d' % n for n in range(0, 11))))
        print("    " + "-"*35)
        index = 0
        for line in matrix:
                newMat += "" + ''.join('%2d' % index) + " : " + str(''.join('%3d' % n for n in line)) + "\n"
                index+=1
#                newMat.append(str("%3d".join(str(line))))
        print(newMat)


def addM(a, b):
    res = []
    for i in range(len(a)):
        row = []
        for j in range(len(a[0])):
            row.append(a[i][j]+b[i][j])
        res.append(row)
    return res

def mulM(a, scalar):
    res = []
    for i in range(len(a)):
        row = []
        for j in range(len(a[0])):
            row.append(a[i][j]*scalar)
        res.append(row)
    return res

g = Grid()
print("Point weights is")


wheatProbs = g.getProbabilityFor(WHEAT)
woodProbs = g.getProbabilityFor(WOOD)
sheepProbs = g.getProbabilityFor(SHEEP)
clayProbs = g.getProbabilityFor(CLAY)
stoneProbs = g.getProbabilityFor(STONE)

totalProbs = g.getTotalProbability()
print("Total probability")
printMatrix(totalProbs)

ZERO_MAT = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


RESOURCE_PROBABILITIES = [g.getProbabilityFor(NONE),
         wheatProbs,
         sheepProbs,
         clayProbs,
         stoneProbs]

ROAD = 0
SETTLEMENT = 1
CITY = 2
DEV_CARD = 3

COSTS = [[0,0,1,0,1,0], # road
         [0,1,1,1,1,0], # settlement
         [0,2,0,0,0,2], # city
         [0,1,0,1,0,1]] # Dev card



def optimizeFor(buildings):
        total = ZERO_MAT
        
        for building in buildings :
                costs = COSTS[building]
                total = addM(total, mulM(RESOURCE_PROBABILITIES[1], costs[1]))
                total = addM(total, mulM(RESOURCE_PROBABILITIES[2], costs[2]))
                total = addM(total, mulM(RESOURCE_PROBABILITIES[3], costs[3]))
                total = addM(total, mulM(RESOURCE_PROBABILITIES[4], costs[4]))

                
        return applyFilter(total, FILTER);


print("-"*50)

print("Brick first strategy")
printMatrix(clayProbs)          # Needed for early on

print("Max settlement strategy")
printMatrix(optimizeFor([SETTLEMENT]))

print("Long term strategy")
printMatrix(optimizeFor([SETTLEMENT, SETTLEMENT, ROAD, ROAD, ROAD, CITY]))

print("Secondary")
printMatrix(optimizeFor([SETTLEMENT, ROAD, ROAD, CITY]))

# an ore strategy needed later when ore is rarer


# tiles = 3, 4, 5, 4, 3


#t = Tile(0, 0, STONE);
#print(str(t.neighborIds))

            

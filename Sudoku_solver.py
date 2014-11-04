#Sudoku Puzzle

class MyException(Exception):
    pass
    
import numpy as np
import csv
import sys


# function to identify which block a cell belngs to
def getBlockIndex(cell):
    if cell in [0,1,2]:
        return 0
    elif cell in [3,4,5]:
        return 1
    elif cell in [6,7,8]:
        return 2
        
#function to determine a list of possible values for each empty cell(r,c) in the puzzle
def getPossibleValues(r,c, complete_list):
    missingInBlock = [x for x in complete_list if not x in blocks[getBlockIndex(r)][getBlockIndex(c)]]
    missingInRow = [x for x in complete_list if not x in A[r,:]]
    missingInColumn = [x for x in complete_list if not x in A[:,c]]
    possibleValues = list(set(missingInBlock) & set(missingInRow) & set(missingInColumn))
    return possibleValues
    


# Run a first iteration to check for possible values
# if there is only one possible value for a cell, assign it to cell
# run a few iterations until the matrix remains unchanged to make sure we covered all obvious possibilities
def basic_solver(A):
    complete_list = [1,2,3,4,5,6,7,8,9];
    count = 0
    while count < 4:
        for r in range(0,9):
            for c in range(0,9):
                if A[r,c] == 0:
                    possibleValues = getPossibleValues(r,c, complete_list)
                    if len(possibleValues) == 1:
                        A[r,c] = possibleValues[0]
                else:
                    continue
        count = count + 1
    else:
        print "Finished basic run"
    return A
    
def guess_solver(A):
    guessA = A
    complete_list = [1,2,3,4,5,6,7,8,9];
    possibleValueDict = dict()
    guessValueDict = dict()
    for r in range(0,9):
        for c in range(0,9):
            if guessA[r,c] == 0:
                possibleValues = getPossibleValues(r,c, complete_list)
                possibleValueDict[r,c] = possibleValues
    for key, value in possibleValueDict.iteritems():
        if len(value) == 1:
            guessA[key(0),key(1)] = value[0]
        elif len(value) > 1:
            # make a guess - assign the first value in list to empty cell
            guess_value = guessValueDict.get(key)
            guess_new = [i for i in value and i not in guess_value]
            guessValueDict[key(0),key(1)] = guess_value.append(guess_new[0])
            guessA[key(0),key(1)] = guess_new[0]
            #we have new puzzle with another block filled, so we use the basic_solver
            guessA = basic_solver(guessA)
            if 0 not in guessA:
                return guessA
            else:
                guessA = guess_solver(guessA)

if __name__ == '__main__':
  if len(sys.argv) == 3:
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    #Read input from csv file   
    #reader=csv.reader(open("/Users/sindhura/Desktop/sudoku/Problem.csv","rb"),delimiter=',')
    reader=csv.reader(open(input_filename,'r'),delimiter=',')
    x=list(reader)
    A=np.matrix(x).astype('int')

    if A.size != 81:
        sys.exit("file incorrectly formatted - must contain 81 digits")

    try:
        #Divide A into 9 submatrices (or 'blocks') - each block is indexed by row and column - 3*3 blocks
        blocks = map(lambda x: np.split(x, 3, 1),
                       np.split(A, 3, 0))
        blocks = np.array(blocks)
        A = basic_solver(A)
        if 0 not in A:
            print A
            np.savetxt(output_filename, A, fmt='%1d',delimiter=',')
        else:
            guessA = guess_solver(A)
    except MyException as e:
        print "Answer\n"
        print A

  else:
    print 'Usage: python sudoku.py sudoku_puzzle sudoku_solution'
    print 'where sudoku_puzzle is the name of the csv file that has 9 rows and 9 numbers in each row separated by a comma with 0 representing missing numbers'
    print 'and sudoku_solution is the name of the output csv file'



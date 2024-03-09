
guessDict = {}
def generateGuessDict():
    with open('./valid-wordle-words.txt') as file:
        count = 1
        for line in file.readlines():
            guessDict[count] = line.removesuffix('\n')
            count += 1

solutionsDict = {}
def generateSolutionDict():
    with open('./valid_solutions.csv') as file:
        count = 1
        for line in file.readlines():
            solutionsDict[count] = line.removesuffix('\n')
            count += 1
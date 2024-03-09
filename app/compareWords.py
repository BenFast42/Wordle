from collections import Counter

#Not perfect, but it does the job
def compareWords(guess: str, ans: str):
    colors = []
    guessOccurrences = Counter(guess)
    ansOccurrences = Counter(ans)

    for letter1, letter2 in zip(guess, ans):
        if letter1 == letter2:
            colors.append('green')
        
        elif guessOccurrences[letter1] <= ansOccurrences[letter1]:
            colors.append('yellow')

        else:
            colors.append('grey')
    return colors






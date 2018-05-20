import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print("  ", len(wordList), "words loaded.")
    return wordList

def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
    score=0
    for x in word:
        score += SCRABBLE_LETTER_VALUES[x]
    score=score*len(word)
    if len(word)==n:
        score=score+50
    return score

def displayHand(hand):
    """
    Displays the letters currently in the hand.

    For example:
    >>> displayHand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print letter,    ## print all on the same line
    print
    
def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    numVowels = n // 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    for x in word:
        hand[x]-=(1)
    return hand

def reverseUpdateHand(hand, word):
    """
    To reverse uodated hand to original states in case player chose to replay.
    
    word: string
    hand: dictionary (string -> int)    
    """
    for x in word:
        hand[x]+=(1)
    return hand

def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    checkWord = {}
    checkWord = getFrequencyDict(word)
    
    if word in wordList:
        for letter in word:
            if letter in hand.keys():
                if checkWord[letter] > hand[letter]:
                    return False
            else:
                return False
    else: 
        return False

    return True

def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    count = 0
    for letter in hand.keys():
        count += hand[letter]
    return count

def playHand(hand, wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      wordList: list of lowercase strings
      n: integer (HAND_SIZE; i.e., hand size required for additional points)
      
    """       
    totalScore = 0                                                     # Keep track of the total score
    playedWords = ""
    while calculateHandlen(hand) > 0:                                  # As long as there are still letters left in the hand:
        displayHand(hand)                                              # Display the hand 
        playWord = str(raw_input("Please enter word or . to quit: "))  # Ask user for input
        if playWord == ".":                                            # If the input is a single period:           
            break                                                      # End the game (break out of the loop)
            
        if isValidWord(playWord, hand, wordList) == False:             # Otherwise (the input is not a single period):
            print "Invalid word, please try again\n"                     # If the word is not valid, reject invalid word 
            print
        else:                                                          # Reject invalid word 
            totalScore += getWordScore(playWord, n)                    # Add score to total
            playedWords += playWord                                    # Tell the user how many points the word earned, and the updated total score, in one line followed by a blank line
            print "\nYou scored %d points with the word" %getWordScore(playWord, n), playWord     
            updateHand(hand, playWord)                                 # Update the hand

    # Game is over (user entered a '.' or ran out of letters), so tell user the total score
    print "Your total score is %d\n\n" %totalScore
    reverseUpdateHand(hand, playedWords)                               # Restore hand in case player wants to replay
    return 

### Playing a game

def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, tell them their input was invalid.
 
    2) When done playing the hand, repeat from step 1    
    """
    numLetters = 0
    hand = {}
    while True:   
        action = str(raw_input("n = New Game \nr = Replay Previous Game\ne = End Game\n\nPlease enter n, r or e: "))
        
        if action == "n":
            while True:
                numLetters = raw_input("Please enter number of letters: ")
                if str.isdigit(numLetters) and int(numLetters) > 0 and int(numLetters) < 16:
                    numLetters = int(numLetters)
                    break
                else:
                    print "Invalid input, please enter a number (1 - 15): \n"
            hand = dealHand(numLetters)
            playHand(hand, wordList, numLetters)       
        elif action == "r":
            if len(hand) == 0:
                print "There is no dealt hand for replay, please choose New Game to begin.\n"
                cont = str(raw_input("Please enter any key to continue...\n"))
            else:
                playHand(hand, wordList, numLetters)
        elif action == "e":
            print "Thanks for playing. Goodbye.\n"
            break
        else:
            print "Invalid input, please try again\n"
            
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)            

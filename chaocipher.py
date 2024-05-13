"""
Chaocipher Encrypter
author: Glenn Gorgoth
date: April 24, 2023

Takes a message and encrypts it using the Chaocipher algorithm. 
Returns the encrypted message, and the cypher Alphabet used to encrypt 
(and needed to decrypt).

"""

import random

def CreateAlphabetList (alphabet):
    # take an alphabet(str), return a list of that alphabet
    lyst = []
    for letter in alphabet:
        lyst.append(letter)
    return lyst

def EncryptLetter(ptLetter, ptLyst, cyLyst):
    # take a Plaintext Letter, returns the cooresponding Cyphertext letter
    try:
        letterIndex = ptLyst.index(ptLetter)
    except ValueError:
        print('unrecognized letter')
        cyLetter = ''
    else:
        cyLetter = cyLyst[letterIndex]
    return cyLetter

def DecryptLetter(letter, ptLyst, cyLyst):
    # Takes a cyphertext letter, returns cooresponding plaintext letter
    letterIndex = cyLyst.index(letter)
    ptLetter = ptLyst[letterIndex]
    return ptLetter

def PermutePtLyst (ptLyst, ptIndex):
    # permutes the Plaintext alphabet according to chaocipher algorithm
    ptIndex += 1
    newLystFront = ptLyst[ptIndex:]
    newLystBack = ptLyst[:ptIndex]
    newLyst = newLystFront + newLystBack
    letterShift = newLyst.pop(2)
    newLyst.insert(13, letterShift)
    print("PT Lyst = ", "".join(newLyst))
    return newLyst

def PermuteCyLyst (cyLyst, cyIndex):
    # Permutes cyphertext alphabet according to chaocipher algorithm
    newLystFront = cyLyst[cyIndex:]
    newLystBack = cyLyst[:cyIndex]
    newLyst = newLystFront + newLystBack
    letterShift = newLyst.pop(1)
    newLyst.insert(13, letterShift)
    print("CY Lyst = ", "".join(newLyst))
    return newLyst

def EncryptPT (ptLyst, cyLyst, ptWord):
    # taks a plaintext message, along with PT alphabet list and cypher-text alphabet,
    # returns the encrypted message
    alphabet ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"  
    count = 1
    cyWord = ""
    for letter in ptWord:
        if letter == " " or letter not in alphabet:
            continue
        newLetter = EncryptLetter(letter, ptLyst, cyLyst)
        cyWord += newLetter
        count += 1
        if count > 5:
            cyWord += " "
            count = 1
        if letter != " ":
            letterIndex = ptLyst.index(letter)
            ptLyst = PermutePtLyst(ptLyst, letterIndex)
            cyLyst = PermuteCyLyst(cyLyst, letterIndex)
    return cyWord

def DecryptCY (ptLyst, cyLyst, cyWord):
    # takes an encrypted message, with accompanying ptLyst(alphabet) and cyLyst(cy alphabet)
    # returns decrypted message
    alphabet ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"  
    count = 1
    ptWord = ""
    for letter in cyWord:
        if letter == " " or letter not in alphabet:
            #if current character isn't an alphabet letter, ignore it
            continue
        newLetter = DecryptLetter(letter, ptLyst, cyLyst)
        ptWord += newLetter
        count += 1
        if letter != " ":
            letterIndex = ptLyst.index(newLetter)
            ptLyst = PermutePtLyst(ptLyst, letterIndex)
            cyLyst = PermuteCyLyst(cyLyst, letterIndex)
    return ptWord

def randomAlphabet (alphabet):
    # generate a randomly ordered alphabet for use as a cypher alphabet
    newAlpha = ""
    maxNum = len(alphabet)
    alphaLyst = list(alphabet)
    for i in range(maxNum):
        nextLetter = alphaLyst.pop(random.randint(0, len(alphaLyst)-1))
        newAlpha += nextLetter
    return newAlpha

def is_good_keyword(keyword):
    # checks to see if the keyword only contains alphabet letters.
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
    good_key = True
    keyword = keyword.upper()
    for i in keyword:
        if i not in alphabet:
            good_key = False
    return good_key

def is_good_shift(shift):
    # checks that the shift only contains numbers
    nums = '1234567890'
    good = True
    for i in shift:
        if i not in nums:
            good = False
    return good 

def createCypherAlphabet(keyword,shift):
    # takes a keyword (str) and a shift value (int)
    # returns a cypherAlphabet rearranged according to the keyword and shift
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphalist = list(alphabet)
    good_key = True
    good_shift = True
    keylist = []
    cypherAlpha = '' 
    if keyword:
        if is_good_keyword(keyword):
            keyword = keyword.upper()
            for k in keyword:
                if k not in keylist:
                    # make a list of the keyword, without doubles
                    keylist.append(k)
        else:
            print('Not a valid keyword. Use only alphabet letters')
            good_key = False
    for i in keylist:
        # Add the keyword letters to the front of the alphabet, removing those same letters
        # from their normal position in the alphabet
        if i in alphalist:
            indx = alphalist.index(i)
            alphalist.pop(indx)
        cypherAlpha += i
    for i in alphalist:
        # add the remaining alphabet letters in their normal order.
        cypherAlpha += i
    newcypherAlpha = cypherAlpha
    if shift:
        if is_good_shift(shift):
            shift = int(shift)%26
            # move the keyword letterns down {shift} many spaces in the alphabet
            keyword = cypherAlpha[:len(keylist)]
            first_half = cypherAlpha[len(keylist):len(keylist)+shift]
            second_half = cypherAlpha[len(keylist)+shift:]
            newcypherAlpha = first_half+keyword+second_half
        else:
            print('not a valid shift number. only use positive integers.')
            good_shift = False
    return newcypherAlpha

def encrypt_init(msg = '',keyword = '',shift = 0):
    # set up the PT and CTalphabets according to keyword and shift
    # encrypt message with cooresponding CTalphabet
    # return encrypted message, keyword, and shift
    plaintextAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plaintextLyst = list(plaintextAlpha)
    if not msg:
        ptMessage = "women who believe in each other create armies that will win kingdoms and wars"
    else:
        ptMessage = msg
    ptMessage = ptMessage.upper()
    cyphertextAlpha = createCypherAlphabet(keyword, shift)
    cyphertextLyst = list(cyphertextAlpha)
    cyMessage = EncryptPT(plaintextLyst, cyphertextLyst, ptMessage)
    print("Encrypted Message = ", cyMessage)
    return cyMessage, keyword, shift

def decrypt_init(msg = '',keyword = '', shift = 0):
    # set up the PT and CTalphabets according to keyword and shift
    # decrypt message with cooresponding CTalphabet
    # return decrypted message, keyword, and shift
    plaintextAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plaintextLyst = list(plaintextAlpha)
    cyphertextAlpha = createCypherAlphabet(keyword, shift)
    cyphertextLyst = list(cyphertextAlpha) 
    msg = msg.upper()
    decrypted_msg = DecryptCY(plaintextLyst, cyphertextLyst, msg)
    return decrypted_msg, keyword, shift

def encrypt_init_v2():
    # old version, maybe can delete this
    plaintextAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plaintextLyst = list(plaintextAlpha)
    plaintext = input("Enter a message you would like to encrypt: ")
    keyword = input("Enter a keyword (alphabet letters only): ")
    while not is_good_keyword(keyword):
        print('Not a valid keyword. Use only alphabet letters.')
        keyword = input("Enter a keyword (alphabet letters only): ")

    shift =  input("Enter a Shift value (positive integer): ")
    while not is_good_shift(shift):
        print('Not a valid shift number. Use only positive integers.')
        shift =  input("Enter a Shift value (positive integer): ")

    if not plaintext:
        ptMessage = "women who believe in each other create armies that will win kingdoms and wars"
    else:
        ptMessage = plaintext
    ptMessage = ptMessage.upper()
    cyphertextAlpha,good_key, good_shift = createCypherAlphabet(keyword, shift)
    print(cyphertextAlpha, good_key, ' ', good_shift)
    cyphertextLyst = list(cyphertextAlpha)
    cyMessage = EncryptPT(plaintextLyst, cyphertextLyst, ptMessage)
    print("Encrypted Message = ", cyMessage)
    return cyMessage, keyword, shift
    
def decrypt_init_v2(cy_package):
    # Old version. Maybe can delete
    plaintextAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plaintextLyst = list(plaintextAlpha)
    print("encrypted message: ",cy_package[0])
    print('keyword: ',cy_package[1])
    print('shift: ',cy_package[2])
    msg = input("Enter an encrypted message: ")
    keyword = input("Enter a keyword (alphabet letters only): ")
    while not is_good_keyword(keyword):
        print('Not a valid keyword. Use only alphabet letters.')
        keyword = input("Enter a keyword (alphabet letters only): ")

    shift =  input("Enter a Shift value (positive integer): ")
    while not is_good_shift(shift):
        print('Not a valid shift number. Use only positive integers.')
        shift =  input("Enter a Shift value (positive integer): ")
    cyphertextAlpha,good_key, good_shift = createCypherAlphabet(keyword, shift)
    print(cyphertextAlpha, good_key, ' ', good_shift)
    cyphertextLyst = list(cyphertextAlpha) 
    decrypted_msg = DecryptCY(plaintextLyst, cyphertextLyst, msg)
    print('Decrypted Message = ',decrypted_msg)
    return decrypted_msg

if __name__ == '__main__':
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plaintextAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plaintextLyst = CreateAlphabetList(plaintextAlpha)
    cyphertextAlpha = randomAlphabet(alphabet)
    # comment out to use the randomalphabet
    cyphertextAlpha = 'SNYGXKUEDIQTCMFLHBJARWPOVZ'

    # cyphertextLyst = list(cyphertextAlpha)
    cyphertextLyst = list(plaintextAlpha)

    plaintext = input("Enter a message you would like to encrypt: ")
    keyword = input("Enter a keyword (alphabet letters only): ")
    while not is_good_keyword(keyword):
        print('Not a valid keyword. Use only alphabet letters.')
        keyword = input("Enter a keyword (alphabet letters only): ")


    shift =  input("Enter a Shift value (positive integer): ")
    while not is_good_shift(shift):
        print('Not a valid shift number. Use only positive integers.')
        shift =  input("Enter a Shift value (positive integer): ")
    
    if plaintext == '' or plaintext == None:
        ptMessage = "women who believe in each other create armies that will win kingdoms and wars"
    else:
        ptMessage = plaintext
    ptMessage = ptMessage.upper()
    cyphertextAlpha,good_key, good_shift = createCypherAlphabet(keyword, shift)
    print(cyphertextAlpha, good_key, ' ', good_shift)
    cyphertextLyst = list(cyphertextAlpha)
    cyMessage = EncryptPT(plaintextLyst, cyphertextLyst, ptMessage)
    print("Encrypted Message = ", cyMessage)
    """
    cy_package = encrypt_init()

    decrypt = input("Decrypt Message? (y/n): ")
    if decrypt == 'y':
        decrypt = True
    else:
        decrypt = False
    if decrypt:
        decrypt_init(cy_package)

        

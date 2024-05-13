import math
import random

# 56 bit table
key_pc_56 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# Number of bit shifts
shift_table = [1, 1, 2, 2,
               2, 2, 2, 2,
               1, 2, 2, 2,
               2, 2, 2, 1]
 
# 48 bit table
key_pc_48 = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32]
 
# Initial Permutation
IP_table = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]
 
# Expansion D-box Table
E_bit_table = [32, 1, 2, 3, 4, 5, 4, 5,
         6, 7, 8, 9, 8, 9, 10, 11,
         12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21,
         22, 23, 24, 25, 24, 25, 26, 27,
         28, 29, 28, 29, 30, 31, 32, 1]
 
# Straight Permutation Table
P_table = [16,  7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2,  8, 24, 14,
       32, 27,  3,  9,
       19, 13, 30,  6,
       22, 11,  4, 25]
 
# S-box Table
S_boxes = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
 
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
 
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
 
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
 
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
 
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
 
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
 
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]
 
# Final Permutation Table
FP_table = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

def CreateSubkeys(key):
    K_64 = getBinary(key)
    K_56 = K_56_perm(K_64)
    C_0 = K_56[:28]
    D_0 = K_56[28:]
    CD_list = []
    c_next = C_0
    d_next = D_0
    for i in range(16):
        shift = shift_table[i]
        c_next,d_next = leftShift(c_next,d_next,shift,i+1)
        CD_list.append(c_next+d_next)
    subkeys = K_48_perm(CD_list)
    return subkeys

def K_56_perm(K_64):
    K_56 = ''
    for i in key_pc_56:
        K_56 += K_64[i-1]
    if debug:
        print(K_56)
    return K_56

def leftShift(C, D, shift, iter):
    C_next = C[shift:] + C[:shift]
    D_next = D[shift:] + D[:shift]
    if debug:
        print('C',iter,' = ',C_next)
        print('D',iter,' = ', D_next)
    return C_next, D_next

def K_48_perm(CD_list):
    K_list = []
    for CD in CD_list:
        newK = ''
        for i in key_pc_48:
            newK += CD[i-1]
        K_list.append(newK)
        if debug:
            print('K',len(K_list),' = ',newK)
    return K_list

def encodeMessage(msg, subkeys, decrypt=False):
    if debug or short_debug:
        print(' *** ENCODING START *** ')
        print('msg: ',msg)
    if decrypt:
        subkeys.reverse()
    encoded_msg = ''
    msg = getBinary(msg)
    if len(msg)<=64:
        encoded_msg = encodeData(msg, subkeys)
    else:
        for block in range(len(msg)//64):
            start = block*64
            end = (block+1)*64
            encoded_msg += encodeData(msg[start:end], subkeys)
    c_msg = bin2hex(encoded_msg)
    c_msg = c_msg.upper()
    if debug:
        print("Encrypted Message = ",c_msg)
    return c_msg
    pass

def encodeData(msg, subkeys):
    M_IP = initial_permutation(msg)
    L_0 = M_IP[:32]
    R_0 = M_IP[32:]
    l_list = [L_0]
    r_list = [R_0]
    for n in range(1,17):
        L_next = r_list[n-1]
        R_next = XOR(l_list[n-1], e_bit(r_list[n-1], subkeys[n-1],n))
        l_list.append(L_next)
        r_list.append(R_next)
    if debug:
        print("L16 = ",L_next)
        print("R16 = ",R_next)
    RL_16 = R_next+L_next
    RL_IP = final_permutation(RL_16)
    return RL_IP
    pass

def final_permutation(RL_16):
    rl_ip = ''
    for i in FP_table:
        rl_ip += RL_16[i-1]
    if debug:
        print("RL_IP = ",rl_ip)
    return rl_ip
    pass

def initial_permutation(msg):
    m = ''
    for i in IP_table:
        m += msg[i-1]
    if debug:
        print('IP = '+m)
    return m
    pass

def e_bit(r,k,iter):
    e = ''
    for i in E_bit_table:
        e += r[i-1]
    if debug:
        print('e(R)',iter,e)
    e_xor = XOR(e,k)
    b_list = []
    for j in range(8):
        k = j*6
        b_list.append(e_xor[k:k+6])
    s = s_box(b_list)
    p = p_perm(s)
    if debug:
        print('s = ',s) 
        print('p = ',p) 
    return p

def p_perm(s):
    p = ''
    for i in P_table:
        p += s[i-1]
    return p

def s_box(b_list):
    msg = ''
    for i in range(8):
        b = b_list[i]
        box = S_boxes[i]
        s = ''
        r = int((b[0]+b[-1]),2)
        c = int(b[1:-1],2)
        s = str(bin(box[r][c]))
        s = padding_binary(s[2:],4)
        if debug:
            print('s_box b = ',b,'s = ',s)
        msg += s
    return msg

def padding_binary(num,min):
    if len(num) < min:
        for i in range(min-len(num)):
            num = '0'+num
    return num

def XOR(a,b):
    y = int(a,2) ^ int(b,2)
    y_xor = '{0:b}'.format(y)
    if len(y_xor)< len(a):
        add0 = ''
        for i in range(len(a)-len(y_xor)):
            add0+='0'
        y_xor = add0 + y_xor
    if debug:
        print('a = ',a)
        print('b = ',b)
        print('y_xor = ',y_xor)
    return y_xor
    pass

hex_chars = 'abcdefABCDEF0123456789'
bin_cars = '01'

def hex2bin(hex_msg):
    bin_msg = "{0:08b}".format(int(hex_msg, 16))
    if len(bin_msg)<len(hex_msg)*4:
        add_zeros = ''
        for i in range(len(hex_msg)*4-len(bin_msg)):
            add_zeros += '0'
        bin_msg = add_zeros + bin_msg
    if debug:
        print('bin_msg = '+bin_msg)
    return bin_msg
    

def bin2hex(bin_msg):
    hd = hd = (len(bin_msg) + 3) // 4
    hex_msg = '{:0{}x}'.format(int(bin_msg, 2), hd)
    if debug:
        print('hex_msg = '+hex_msg)
    return hex_msg

def getBinary(msg):
    if isAscii(msg):
        msg = ascii2hex(msg)
    if isHex(msg):
        msg = checkHexLength(msg)
        if debug or short_debug:
            print('hex version: ',msg)
        msg = hex2bin(msg)
    if debug or short_debug:
        print('bin version: ',msg)
    return msg

def checkHexLength(msg):
    pad_count = len(msg)%16
    if pad_count:
        pad_count = 16-pad_count
        # print('Padding Hex Message with ',pad_count,' zeros')
        for x in range(pad_count):
            msg+='0'
    return msg

def isBinary(msg):
    msg = str(msg)
    for i in msg:
        if i not in bin_cars:
            return False
    return True

def isHex(msg):
    msg = str(msg)
    for i in msg:
        if i not in hex_chars:
            return False
    return True

def isAscii(msg):
    msg = str(msg)
    for i in msg:
        if i not in hex_chars:
            return True    
    return False

def ascii2hex(msg):
    hex_msg = ''
    for i in msg:
        hex_msg+= format(ord(i),'x')
    return hex_msg+'0D0A'

def hex2ascii(msg):
    return bytearray.fromhex(msg).decode()
    
def getRandomKey():
    randomKey = ''
    for i in range(16):
        randomKey += hex_chars[random.randrange(len(hex_chars)-1)]
    randomKey = randomKey.upper()
    return randomKey

def runDES(message, key=None, decrypt=False, back2ascii=False):
    #for running on the website
    if not key:
        key = getRandomKey()
    subkeys = CreateSubkeys(key)
    C_msg = encodeMessage(message, subkeys, decrypt)
    if back2ascii:
        C_msg = hex2ascii(C_msg)
        print ('asciiMsg = ',C_msg)
        # try:
        #     C_msg = hex2ascii(C_msg)
        # except:
        #     pass
    return C_msg, key


def DES(message,key=None, decrypt=False):
    back2ascii = isAscii(message)
    if not key:
        key = getRandomKey()
    subkeys = CreateSubkeys(key)
    C_msg = encodeMessage(message, subkeys, decrypt)
    D_msg = encodeMessage(C_msg, subkeys, True)
    print()
    print('Original Message: ', message)
    print('Key: ',key)
    print('Encrypted Message: ', C_msg)
    print('Decrypted Message: ', D_msg)
    if back2ascii:
        try:
            print('Decrypted in Ascii: ', hex2ascii(D_msg))
        except:
            pass
    print('* * * * * * * * * * * * *')
    print()
    return C_msg, key

def batchTest():
    messages = [
        "0123456789ABCDEF",
        "6D6573736167652E",
        "Your lips are smoother than vaseline",
        "The DES (Data Encryption Standard) algorithm is the most widely used encryption algorithm in the world."
    ]
    keys = [
        "133457799BBCDFF1",
        "0E329232EA6D0D73",
       getRandomKey()
    ]
    for message in messages:

        back2ascii = isAscii(message)
        for key in keys:
            DES(message,key)

debug = False
short_debug = False

if __name__ == '__main__':
    # batchTest()
    DES('0123456789ABCDEF','133457799BBCDFF1')
    DES('abcdefghijklmnop')
    DES('Please make your input variable so that other inputs also work.')




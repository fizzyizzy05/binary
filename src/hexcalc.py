# Library for converting between decimal and binary values
import math
def dec2hex(input):
    decimal = True
    
    # Make sure the input is a number
    for char in str(input):
        if char.isdecimal() == False:
            decimal = False
            break
        
    if decimal == False:
        return "char"
    else:
        q = int(input) * 16 # Quotient
        r = 0 # Remainder
        result = ""
        ansBits = []
        
        while q > 0:
            r = q % 16
            q = q // 16
            ansBits.append(str(r))
            
        for x in range (len(ansBits) - 1, 0, -1):
            if ansBits[x] == "10":
                result = result + "A"
            elif ansBits[x] == "11":
                result = result + "B"
            elif ansBits[x] == "12":
                result = result + "C"
            elif ansBits[x] == "13":
                result = result + "D"
            elif ansBits[x] == "14":
                result = result + "E"
            elif ansBits[x] == "15":
                result = result + "F"
            else:
                result = result + ansBits[x]
            
        return result

def hex2dec(input):
    hexadecimal = True
    
    # Make sure the input is a valid hexadecimal digit
    for char in str(input):
        try:
            int(char, 16)
        except:
            hexadecimal = False
            break
    
    if hexadecimal == False:
        return "char"
    else:
        input = str(input).upper()
        result = 0
        ansBits = []
        power = int(len(input) - 1)

        for char in input:
            if char == "A":
                char = 10
                ansBits.append(char * (math.pow(16, power)))
            elif char == "B":
                char = 11
                ansBits.append(char * (math.pow(16, power)))
            elif char == "C":
                char = 12
                ansBits.append(char * (math.pow(16, power)))
            elif char == "D":
                char = 13
                ansBits.append(char * (math.pow(16, power)))
            elif char == "E":
                char = 14
                ansBits.append(char * (math.pow(16, power)))
            elif char == "F":
                char = 15
                ansBits.append(char * (math.pow(16, power)))
            else:
                char = int(char)
                ansBits.append(char * (math.pow(16, power)))
                
            power = power - 1
            
        for x in ansBits:
            result += x
            
        return str(int(result))

def hex2bin(input):
    hexadecimal = True
    result = ""

    # Make sure the input is a valid hexadecimal digit
    for char in str(input):
        try:
            int(char, 16)
        except:
            hexadecimal = False
            break

    if hexadecimal == False:
        return "char"
    else:
        for char in str(input):
            if char == '0':
                result += "0000"
            elif char == '1':
                result += "0001"
            elif char == '2':
                result += "0010"
            elif char == '3':
                result += "0011"
            elif char == '4':
                result += "0100"
            elif char == '5':
                result += "0101"
            elif char == '6':
                result += "0110"
            elif char == '7':
                result += "0111"
            elif char == '8':
                result += "1000"
            elif char == '9':
                result += "1001"
            elif char == 'A':
                result += "1010"
            elif char == 'B':
                result += "1011"
            elif char == 'C':
                result += "1100"
            elif char == 'D':
                result += "1101"
            elif char == 'E':
                result += "1110"
            elif char == 'F':
                result += "1111"

    return str(result).lstrip('0')

def bin2hex(input):
    binary = True

    for char in str(input):
        if char != '1' and char != '0':
            binary = False
            break

    if binary == False:
        return "char"
    else:
        ans = hex(int(input, 2))
        return str(ans).lstrip("0x").upper()

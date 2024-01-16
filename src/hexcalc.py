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

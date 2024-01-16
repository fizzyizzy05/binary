# Library for working out binary and decimal values. Using the same file for both
def hello():
    print("Hello World")

def bin2dec(input):
    ans = 0
    mult =  1

    # Work out how many bits the binary input is, and work out the largest bits value
    for count in range (len(input) - 1):
        mult = mult * 2

    for char in input:
        if char == '1':
            ans += mult
        elif char != '1' and char != '0':
            return "char"

        mult = mult / 2

    return int(ans)

def dec2bin(input):
    decimal = True

    # Make sure the input is a number
    for char in input:
        if char.isdecimal() == False:
            decimal = False
            break

    if decimal == False:
        return "char"
    else:
        q = int(input) * 2 # Quotient
        r = 0 # Remainder
        result = ""
        ansBits = []

        while q > 0:
            r = q % 2
            q = q // 2
            ansBits.append(str(r))

        for x in range (len(ansBits) - 1, 0, - 1):
            result = result + ansBits[x]

        return result

def bitCount(input):
    bits = []
    mult = 1

    # Work out how many bits the binary input is, and work out the largest bits value
    for count in range (len(input) -1):
        mult = mult * 2

    # For each bit, add a value to the bit counter
    for char in input:
        bits.append(int(mult))
        mult = mult / 2

    bitStr = str(bits).strip('[')
    bitStr = bitStr.strip(']')

    return bitStr

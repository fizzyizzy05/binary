# Library for working out binary and decimal values. Using the same file for both
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

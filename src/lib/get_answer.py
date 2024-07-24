# This script returns the answer of a calculation to the main window.
def get_answer(input, in_base, out_base):
    # 0 = Binary
    # 1 = Decimal
    # 2 = Hexadecimal
    # 3 = Octal
    # No input
    # Binary to Decimal
    if in_base == 0 and out_base == 1:
        try:
            int(input, 2)
        except:
            return "char"
        ans = int(input, 2)
        return str(int(input, 2))
    # Decimal to Binary
    elif in_base == 1 and out_base == 0:
        try:
            int(input, 10)
        except:
            return "char"
        ans = bin(int(input)).lstrip("0b")
        return ans
    # Decimal to Hexadecimal
    elif in_base == 1 and out_base == 2:
        try:
            int(input)
        except:
            return "char"
        ans = hex(int(input)).lstrip("0x").upper()
        return ans
    # Hexadecimal to Decimal
    elif in_base == 2 and out_base == 1:
        try:
            int(input, 16)
        except:
            return "char"
        ans = str(int(input, 16))
        return ans
    # Hexadecimal to Binary
    elif in_base == 2 and out_base == 0:
        try:
            int(input, 16)
        except:
            return "char"
        ans = bin(int(input, 16)).lstrip("0b")
        return ans
    # Binary to Hexadecimal
    elif in_base == 0 and out_base == 2:
        try:
            int(input, 2)
        except:
            return "char"
        ans = hex(int(input, 2)).strip("0x").upper()
        return ans
    # Oct to Bin
    elif in_base == 3 and out_base == 0:
        for char in str(input):
            try:
                int(char, 8)
            except:
                return "char"
        ans = str(bin(int(input, 8)).lstrip("0b"))
        return ans
    # Bin to Oct
    elif in_base == 0 and out_base == 3:
        try:
            int(input, 2)
        except:
            return "char"
        ans = str(oct(int(input, 2)).lstrip("0o"))
        return ans
    # Oct to Dec
    elif in_base == 3 and out_base == 1:
        try:
            int(input, 8)
        except:
            return "char"
        ans = str(int(input, 8))
        return ans
    # Dec to Oct
    elif in_base == 1 and out_base == 3:
        try:
            int(input, 10)
        except:
            return "char"
        ans = str(oct(int(input)).lstrip("0o"))
        return ans
    # Oct to Hex
    elif in_base == 3 and out_base == 2:
        try:
            int(input, 8)
        except:
            return "char"
        ans = hex(int(input, 8)).lstrip("0x").upper()
        return ans
    # Hex to Oct
    elif in_base == 2 and out_base == 3:
        try:
            int(input, 16)
        except:
            return "char"
        ans = oct(int(input, 16)).lstrip("0o")
        return ans
    # Same number bases
    elif in_base == out_base:
        # Set the output label to be the same as the input
        if in_base == 0:
            try:
                int(input, 2)
                return input
            except:
                return "char_dual"
        elif self.in_dropdown.get_selected() == 1:
            try:
                int(input, 10)
                return input
            except:
                return "char_dual"
        elif self.in_dropdown.get_selected() == 2:
            try:
                int(input, 16)
                return input
            except:
                return "char_dual"
        elif self.in_dropdown.get_selected() == 3:
            try:
                int(input, 8)
                return input
            except:
                return "char_dual"

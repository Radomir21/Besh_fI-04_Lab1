import array as arr

w = 32
b = 2 ** w


def convert_from_hex(number):
    if number == '0':
        return arr.array('I', [0])

    number_int = int(number, 16)
    result = arr.array('I', [])
    while number_int > 0:
        result.append(number_int % b)
        number_int = number_int // b
    result.reverse()
    return result

def convert_to_hex(number):
    if number == [0]:
        return '0'
    number_copy = number[:]
    number_copy.reverse()
    number_int = 0
    for index, digit in enumerate(number_copy):
        number_int += digit * (b ** index)
    n_hex = hex(number_int)
    return n_hex[2:]






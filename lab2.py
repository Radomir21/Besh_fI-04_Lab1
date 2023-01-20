from lab1 import *
from random import choices

A = '12312312abbcadbcabbcabadbcbaebbfebbbcebfbaebcbebfbbbefbcbbefcbeafbfbe2312031293812742712041204fffffffffffffffffffffff'
A1 = '12312312abbcadbcabbcabadbcbaebbfebbbcebfbaebcbebfbbbefbcbbefcbeafbfbe2312031293812742712041204'
B = 'acdcdaacd12312abbca12312312fffefcfefcfcefcffdfeffcffe'


def hex_to_bin(a: str):
    bin = ''
    for char in a.lower():
        match char:
            case '0':
                bin += '0000'
            case '1':
                bin += '0001'
            case '2':
                bin += '0010'
            case '3':
                bin += '0011'
            case '4':
                bin += '0100'
            case '5':
                bin += '0101'
            case '6':
                bin += '0110'
            case '7':
                bin += '0111'
            case '8':
                bin += '1000'
            case '9':
                bin += '1001'
            case 'a':
                bin += '1010'
            case 'b':
                bin += '1011'
            case 'c':
                bin += '1100'
            case 'd':
                bin += '1101'
            case 'e':
                bin += '1110'
            case 'f':
                bin += '1111'
    return bin.upper()


def bin_to_hex(a: str):
    a = a.lstrip('0').lower()
    a = '0' * ((4 - len(a) % 4) % 4) + a
    chunks = [a[i:i + 4] for i in range(0, len(a), 4)]
    hex = ''
    for chunk in chunks:
        match chunk:
            case '0000':
                hex += '0'
            case '0001':
                hex += '1'
            case '0010':
                hex += '2'
            case '0011':
                hex += '3'
            case '0100':
                hex += '4'
            case '0101':
                hex += '5'
            case '0110':
                hex += '6'
            case '0111':
                hex += '7'
            case '1000':
                hex += '8'
            case '1001':
                hex += '9'
            case '1010':
                hex += 'a'
            case '1011':
                hex += 'b'
            case '1100':
                hex += 'c'
            case '1101':
                hex += 'd'
            case '1110':
                hex += 'e'
            case '1111':
                hex += 'f'
    return hex.upper()


def log_ceil(a: str):
    a = a.lstrip('0')
    a_bin = hex_to_bin(a).lstrip('0')
    log = bin(len(a_bin))[2:]
    return bin_to_hex(log)


def barrett(a: str, mod: str):
    a = a.lstrip('0')
    a_bin = convert_from_hex(a)
    mod = mod.lstrip('0')
    mod_bin = convert_from_hex(mod)
    if len(a) >= 2 * len(mod):
        print('div modulo')
        mod_div = long_div_mod(a_bin, mod_bin)[0]
        mul = long_mul(mod_div, mod_bin)
        sub = long_sub(a_bin, mul)
        result = convert_to_hex(sub)
        return result
    else:
        print('barrett modulo')
        four = convert_from_hex('4')
        k = convert_from_hex(log_ceil(mod))
        four_pow_k = long_power2(four, k)
        r = long_div_mod(four_pow_k, mod_bin)[0]
        mul = long_mul(long_div_mod(long_mul(a_bin, r), four_pow_k)[0], mod_bin)
        t = long_sub(a_bin, mul)
        if long_compare(mod_bin, t):
            return convert_to_hex(t)
        else:
            t = long_sub(t, mod_bin)
            return convert_to_hex(t)


print(barrett(A, B))
print(barrett(A1, B), '\n\n')

a = 'D4D2110984907B5625309D956521BAB4157B8B1ECE04043249A3D379AC112E5B9AF44E721E148D88A942744CF56A06B92D28A0DB950FE4CED2B41A0BD38BCE7D0BE1055CF5DE38F2A588C2C9A79A75011058C320A7B661C6CE1C36C7D870758307E5D2CF07D9B6E8D529779B6B2910DD17B6766A7EFEE215A98CAC300F2827DB'
b = '30A120B609DCBE28B09CA92E12DD29D77AE6400DC22B026AFB5FB945AAF62B57F4E48BD299261F02BBB35DD2495B5CD2713BF0E30192DAE1B334659160C8552423F0AD'

print(barrett(a, b))

for i in range(10):
    a = ''.join(choices('0123456789abcdef', k=32)).lstrip('0')
    mod = ''.join(choices('123456789abcdef', k=17))
    barr = barrett(a, mod)
    a_bin = convert_from_hex(a)
    mod_bin = convert_from_hex(mod)
    mod_div = long_div_mod(a_bin, mod_bin)[0]  # a/mod
    mul = long_mul(mod_div, mod_bin)  # (a/mod)*mod
    sub = long_sub(a_bin, mul)  # a - (a/mod)*mod
    result = convert_to_hex(sub)
    if result == barr:
        print(f'try {i} success')
    else:
        raise Exception('ERROR!')

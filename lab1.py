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


def make_equal_length(num1, num2):
    leading_zeros = abs(len(num1) - len(num2))
    if len(num1) < len(num2):
        num1[:0] = arr.array('I', ([0] * leading_zeros))
    else:
        num2[:0] = arr.array('I', ([0] * leading_zeros))


def long_add(num1, num2):
    if len(num1) != len(num2):
        make_equal_length(num1, num2)
    carry = 0
    n = len(num1)
    result = arr.array('I', [0] * n)
    for i in reversed(range(n)):
        temp = num1[i] + num2[i] + carry
        result[i] = temp & (b - 1)
        carry = temp >> w
    if carry != 0:
        result.insert(0, carry)
    return result


def long_sub(num1, num2, base=b):
    if len(num1) != len(num2):
        make_equal_length(num1, num2)
    borrow = 0
    n = len(num1)
    result = arr.array('I', [0] * n)
    for i in reversed(range(n)):
        temp = num1[i] - num2[i] - borrow
        if temp >= 0:
            result[i] = temp
            borrow = 0
        else:
            result[i] = base + temp
            borrow = 1
    if borrow != 0:
        raise ValueError("Negative number!")
    else:
        return result


def long_compare(num1, num2):
    if len(num1) != len(num2):
        make_equal_length(num1, num2)
    n = len(num1)
    i = 0
    while num1[i] == num2[i]:
        i += 1
        if i == n:
            cut_leading_zeros(num1)
            cut_leading_zeros(num2)
            return 0
    if num1[i] > num2[i]:
        cut_leading_zeros(num1)
        cut_leading_zeros(num2)
        return 1
    else:
        cut_leading_zeros(num1)
        cut_leading_zeros(num2)
        return -1


def long_mul_one_digit(num, digit):
    n = len(num)
    result = arr.array('I', [0] * n)
    carry = 0
    for i in reversed(range(n)):
        temp = num[i] * digit + carry
        result[i] = temp & (b - 1)
        carry = temp >> w
    if carry != 0:
        result.insert(0, carry)
    return result


def long_shift_digits_to_high(num, k):
    num.extend([0] * k)


def long_mul(num1, num2):
    result = arr.array('I', [0])
    n = len(num2)
    for i in reversed(range(n)):
        temp = long_mul_one_digit(num1, num2[i])
        long_shift_digits_to_high(temp, n - i - 1)
        result = long_add(result, temp)
    return result


def long_square(num):
    return long_mul(num, num)


def cut_leading_zeros(num):
    while num[0] == 0 and len(num) != 1:
        num.pop(0)


def pad_leading_zeros(num):
    while len(num) % w != 0:
        num.insert(0, 0)


def convert_base_b_to_bin(num):
    result = arr.array('I', [])
    for digit in num:
        digit_as_bin = format(digit, f'0{w}b')  # конвертируем цифру в бинарную систему длинной w бит 
        result.extend(arr.array('I', list(map(int, [*digit_as_bin]))))  # склеиваем результаты в порядке старшинства
    cut_leading_zeros(result)
    return result


def convert_bin_to_base_b(num):
    pad_leading_zeros(num)
    digits_bin = [''.join(map(str, num[i:i + w])) for i in
                  range(0, len(num), w)]  # разделяем число на отрезки длинной w бит
    result = arr.array('I', [int(digit, 2) for digit in digits_bin])  # конвертируем каждый отрезок в цифру 
    return result


def long_shift_bits_to_high(num, k):
    num_copy = num[:]
    long_shift_digits_to_high(num_copy, k)
    return num_copy


def long_div_mod(num1, num2):
    num1_bin = convert_base_b_to_bin(num1)
    num2_bin = convert_base_b_to_bin(num2)
    k = len(num2_bin)
    r = num1_bin[:]
    q = arr.array('I', [])
    while long_compare(r, num2_bin) != -1:
        t = len(r)
        c = long_shift_bits_to_high(num2_bin, t - k)
        if long_compare(r, c) == -1:
            t -= 1
            c = long_shift_bits_to_high(num2_bin, t - k)
        r = long_sub(r, c, base=2)
        cut_leading_zeros(r)
        q = long_add(q, arr.array('I', [1] + [0] * (t - k)))
    q_base_b = convert_bin_to_base_b(q)
    r_base_b = convert_bin_to_base_b(r)
    return q_base_b, r_base_b


def long_power2(num, power):
    power_bin = convert_base_b_to_bin(power)
    m = len(power_bin)
    result = arr.array('I', [1])
    for i in range(m):
        if power_bin[i] == 1:
            result = long_mul(result, num)
        if i != m - 1:
            result = long_mul(result, result)
    return result


def tests(num1, num2, num3):
    A_plus_B = long_add(num1, num2)
    C_x_A_plus_B = long_mul(num3, A_plus_B)
    A_plus_B_x_C = long_mul(A_plus_B, num3)
    A_mul_C = long_mul(num1, num3)
    B_mul_C = long_mul(num2, num3)
    A_mul_C_plus_B_mul_C = long_add(A_mul_C, B_mul_C)
    print("-----------TESTS---------------")
    if long_compare(C_x_A_plus_B, A_mul_C_plus_B_mul_C) == 0 and long_compare(A_plus_B_x_C, C_x_A_plus_B) == 0:
        print("(a + b)* c = c*(a + b) = a*c + b*c   TRUE")
    else:
        print("(a + b)* c = c*(a + b) = a*c + b*c   FALSE")


if __name__ == '__main__':
    A = 'D4D2110984907B5625309D956521BAB4157B8B1ECE04043249A3D379AC112E5B9AF44E721E148D88A942744CF56A06B92D28A0DB950FE4CED2B41A0BD38BCE7D0BE1055CF5DE38F2A588C2C9A79A75011058C320A7B661C6CE1C36C7D870758307E5D2CF07D9B6E8D529779B6B2910DD17B6766A7EFEE215A98CAC300F2827DB'
    B = '3A7EF2554E8940FA9B93B2A5E822CC7BB262F4A14159E4318CAE3ABF5AEB1022EC6D01DEFAB48B528868679D649B445A753684C13F6C3ADBAB059D635A2882090FC166EA9F0AAACD16A062149E4A0952F7FAAB14A0E9D3CB0BE9200DBD3B0342496421826919148E617AF1DB66978B1FCD28F8408506B79979CCBCC7F7E5FDE7'
    C = '269D7722EA018F2AC35C5A3517AA06EAA1949059AE8240428BBFD0A8BE6E2EBF91223991F80D7413D6B2EB213E7122710EDEC617460FA0191F3901604619972018EBEF22D81AED9C56424014CADCC2CCDEE67D36A54BFC500230CA6693ABA057B374746622341ED6D52FE5A79E6860F54F197791B3FEF49FD534CB2C675B6BDB'
    A_plus_B_expected = '10F51035ED319BC50C0C4503B4D44872FC7DE7FC00F5DE863D6520E3906FC3E7E8761505118C918DB31AADBEA5A054B13A25F259CD47C1FAA7DB9B76F2DB450861BA26C4794E8E3BFBC2924DE45E47E5408536E3548A03591DA0556D595AB78C55149F45170F2CB7736A46976D1C09BFCE4DF6EAB040599AF235968F8070E25C2'
    A_sub_B_expected = '9A531EB436073A5B899CEAEF7CFEEE386318967D8CAA2000BCF598BA51261E38AE874C932360023620DA0CAF90CEC25EB7F21C1A55A3A9F327AE7CA879634C73FC1F9E7256D38E258EE860B509506BAE185E180C06CC8DFBC23316BA1B357240BE81B14C9EC0A25A73AE85C0049185BD4A8D7E29F9F82A7C2FBFEF68174229F4'
    A_mul_B_expected = '30A120B609DCBE28B09CA92E12DD29D77AE6400DC22B026AFB5FB945AAF62B57F4E48BD299261F02BBB35DD2495B5CD2713BF0E30192DAE1B334659160C8552423F0AD7FB82870920DF4E9B57980EAD2ADA9F3EF4B5D0718AB7F1053700395278998CB9AD48498D65150E3E837B0BB169D432B441424557061F838A17C65F90A31105F599BF69B87485BF9C70F51D37A417E476E372558C26782AC8C8F35C3D1227E851D8A72CD708700FD90C5E17F22C4EA15730345E56BD76F04B54580813CBE306B4404C6F34BCD9840D2911E6B3CF6DE3EE428C274EDF0A97335D8256DA26FCD67BA5450593A15F6B527ECE76FBBE20F7A882347614AF4B7FAF55086659D'

    N = '50'

    A_base_b = convert_from_hex(A)
    B_base_b = convert_from_hex(B)
    C_base_b = convert_from_hex(C)
    N_base_b = convert_from_hex(N)

    A_plus_B = convert_to_hex(long_add(A_base_b, B_base_b))
    A_sub_B = convert_to_hex(long_sub(A_base_b, B_base_b))
    A_mul_B_base_b = long_mul(A_base_b, B_base_b)
    A_mul_B = convert_to_hex(A_mul_B_base_b)
    A_sqr = convert_to_hex(long_square(A_base_b))

    Q, R = long_div_mod(A_mul_B_base_b, B_base_b)
    A_mul_B_div_B = convert_to_hex(Q)
    A_pow_N = convert_to_hex(long_power2(A_base_b, N_base_b))

    print("\nA+B=", A_plus_B)
    print("A+B=", A_plus_B_expected.lower())
    print("Correct:", A_plus_B_expected.lower() == A_plus_B)

    print("\nA-B=", A_sub_B)
    print("A-B=", A_sub_B_expected.lower())
    print("Correct:", A_sub_B_expected.lower() == A_sub_B)

    print("\nAxB=", A_mul_B)
    print("AxB=", A_mul_B_expected.lower())
    print("Correct:", A_mul_B_expected.lower() == A_mul_B)

    print("\nA^2=", A_sqr)

    print("\n(AxB)/B=", A_mul_B_div_B)
    print("   A   =", A.lower())
    print("Correct:", A.lower() == A_mul_B_div_B)

    print("\nA^N=", A_pow_N)

    tests(A_base_b, B_base_b, C_base_b)

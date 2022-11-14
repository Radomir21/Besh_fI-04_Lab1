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
                  range(0, len(num), w)]  #разделяем число на отрезки длинной w бит
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



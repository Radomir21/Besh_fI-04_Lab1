from matrix import get_matrix


class Normal:
    length = 179
    matrix = get_matrix(length)

    def __init__(self, bin: str) -> None:
        bin = bin.lstrip('0')
        if len(bin) > self.length:
            raise Exception('Invalid initial string!')
        for bit in bin:
            if bit != '1' and bit != '0':
                raise Exception('Invalid initial string!')
        missing_zeroes = self.length - len(bin)
        self.bin = '0' * missing_zeroes + bin

    def __add__(self, other: 'Normal') -> 'Normal':
        result = ''
        for i in range(self.length):
            if self.bin[i] == other.bin[i]:
                result = result + '0'
            else:
                result = result + '1'
        return Normal(result)

    def __lshift__(self, shifts: int) -> 'Normal':
        if 0 <= shifts < self.length:
            bin = self.bin
            first = bin[0:shifts]
            shifted = bin[shifts:] + first
            return Normal(shifted)
        else:
            raise Exception('Invalid shifts!')

    def __repr__(self) -> str:
        stripped = self.bin.lstrip('0')
        return '0' if stripped == '' else stripped

    def __mul__(self, other: 'Normal') -> 'Normal':
        result = ''
        for i in range(self.length):
            left = self << i
            right = other << i
            left_mul = self.left_mul(left)
            right_mul = self.right_mul(left_mul, right)
            result = result + right_mul
        return Normal(result)

    def left_mul(self, left: 'Normal') -> str:
        left_mul = ''
        for i in range(self.length):
            store = 0
            for j in range(self.length):
                store = (store + (int(left.bin[j]) * int(self.matrix[i][j]))) % 2
            left_mul = left_mul + str(store)
        return left_mul

    def right_mul(self, left_mul: str, right: 'Normal') -> str:
        right_mul = 0
        for i in range(self.length):
            right_mul = (right_mul + (int(left_mul[i]) * int(right.bin[i]))) % 2
        return str(right_mul)

    def __pow__(self, power: int) -> 'Normal':
        if power >= 0:
            result = Normal('1' * self.length)
            for i in range(power):
                result = result * self
            return result
        else:
            raise Exception('Invalid power!')


a = Normal('1101010101001001010101111111111111100101001')
b = Normal('1110100000011010100110010110101')
c = Normal('11100001010101')
check = ((a * b) * (a * b) + c) * ((a * b) * (a * b) + c)
print(check)
if str(check) == str((((a * b) ** 2) + c) ** 2):
    print('success')

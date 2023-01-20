class Polynomial:
    length = 179
    generator = '10111'

    def __init__(self, bin: str) -> None:
        bin = bin.lstrip('0')
        for bit in bin:
            if bit != '1' and bit != '0':
                raise Exception('Invalid initial string!')
        if len(bin) <= self.length:
            missing_zeroes = self.length - len(bin)
            self.bin = '0' * missing_zeroes + bin
        else:
            exceeded = bin[:len(bin) - self.length]
            result = bin[len(bin) - self.length:]
            result = Polynomial(result)
            generator = Polynomial(self.generator)
            for i in range(len(exceeded)):
                if exceeded[i] == '1':
                    shifted = generator << (len(exceeded) - i - 1)
                    result = result + shifted
            self.bin = result.bin

    def __add__(self, other: 'Polynomial') -> 'Polynomial':
        result = ''
        for i in range(self.length):
            if self.bin[i] == other.bin[i]:
                result = result + '0'
            else:
                result = result + '1'
        return Polynomial(result)

    def __lshift__(self, shifts: int) -> 'Polynomial':
        if shifts >= 0:
            shifted = self.bin + '0' * shifts
            return Polynomial(shifted)
        else:
            raise Exception('Invalid shifts!')

    def __repr__(self) -> str:
        stripped = self.bin.lstrip('0')
        return '0' if stripped == '' else stripped

    def __mul__(self, other: 'Polynomial') -> 'Polynomial':
        result = Polynomial('0')
        for i in range(self.length):
            if self.bin[i] == '1':
                single_multiplication = other << (self.length - i - 1)
                result = result + single_multiplication
        return result

    def __pow__(self, power: int) -> 'Polynomial':
        if power >= 0:
            result = Polynomial('1')
            for i in range(power):
                result = result * self
            return result
        else:
            raise Exception('Invalid power!')


A = Polynomial(
    '1010010001100010101010011111011000010111100000101011010001000100100011000000010110111001000011010110111001001001100011101111010010000111011000000011010100111100111111110010011')
B = Polynomial('1111001100101000100001000010010010001001111011110000011101100000')

AplusB = '1010010001100010101010011111011000010111100000101011010001000100100011000000010110111001000011010110111001001000011010001010010110001111001010010010011011100010111100011110011'
AxB = '10111111101100111011111110101011100010111100001110111101111011001100110101001101111110010101110010010100001010010110101110110101001011010111011011100011000000000111100110010001110'
Apow35 = '1101100000101100011110000001010100001110101000010011011101100110101000010101001000001000111101011100010001001111001101011000111000010111000011000001110101111000011010011010010001'

if AplusB == str(A + B):
    print('correct sum')
if AxB == str(A * B):
    print('correct product')
if Apow35 == str(A ** 35):
    print('correct power')

class SimpleDes:
    __p8_key = [6, 3, 7, 4, 8, 5, 10, 9]
    __p10_key = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]

    def __init__(self, text: str, key: str):
        self.__text = text
        self.__key = key

    def permutation_10_bits(self, key: str) -> (str, str):
        permutation_string = str()

        for index in self.__p10_key:
            permutation_string += key[index - 1]

        half = int(len(permutation_string) / 2)

        return permutation_string[0:half], permutation_string[half:]

    def left_shift(self, value: str):
        head = value[0]

        tail = value[1:]

        return tail + head

    def permutation_8_bits(self, key: str) -> str:
        permutation_string = str()

        for index in self.__p8_key:
            permutation_string += key[index - 1]

        return permutation_string

    def make_keys(self):
        left, right = self.permutation_10_bits(self.__key)

        left_shift = self.left_shift(left)

        right_shift = self.left_shift(right)

        k1 = left_shift + right_shift

        k1 = self.permutation_8_bits(k1)

        left_shift = self.left_shift(self.left_shift(left_shift))

        right_shift = self.left_shift(self.left_shift(right_shift))

        k2 = left_shift + right_shift

        k2 = self.permutation_8_bits(k2)

        return k1, k2
    

if __name__ == '__main__':
    key = "1010000010"

    print(len(key))

    sim = SimpleDes("adsadsa", key)

    print(sim.make_keys())

    pass

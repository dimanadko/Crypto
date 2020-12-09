import requests
import json
import math
import functools

PLAYER_ID = 221
FINISH_AMOUNT = 1000000


class MakeMeRich():
    def __init__(self):
        """Constructor"""
        self.numberList = []
        self.multiplier = None
        self.modulus = None
        self.increment = None
        self.seed = None
        self.money = 0;

    def egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, x, y = self.egcd(b % a, a)
            return (g, y - (b // a) * x, x)

    def modinv(self, b, n):
        # print('modinv')
        # print(b, n)
        g, x, _ = self.egcd(b, n)
        if g == 1:
            return x % n
        return 0

    def crack_unknown_increment(self, modulus, multiplier):
        increment = (self.numberList[1] - self.numberList[0] * multiplier) % modulus
        self.increment = increment
        # print('Increment ' + str(increment))
        return modulus, multiplier, increment

    def crack_unknown_multiplier(self, modulus):
        multiplier = (self.numberList[2] - self.numberList[1]) \
                     * self.modinv(self.numberList[1] - self.numberList[0], modulus) \
                     % modulus
        self.multiplier = multiplier
        # print('Multiplier ' + str(multiplier))
        return self.crack_unknown_increment(modulus, multiplier)

    def crack_unknown_modulus(self):
        diffs = [s1 - s0 for s0, s1 in zip(self.numberList, self.numberList[1:])]
        zeroes = [t2 * t0 - t1 * t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
        modulus = abs(functools.reduce(math.gcd, zeroes))
        self.modulus = modulus;
        # print('Modulus '+str(modulus))
        return self.crack_unknown_multiplier(modulus)

    def bet(self, amount=1, mode='Lcg', number=1):
        r = requests.get('http://95.217.177.249/casino/playLcg?id=221&bet='+str(amount)+'&number='+str(number)).json()
        print(r)
        self.numberList.append(r['realNumber'])
        if(len(self.numberList)>6):
            self.numberList.pop(0)
        self.money = r['account']['money']
        return r['realNumber'], r['account']['money'], r['message'],

    def initial_start(self):
        for i in range(6):
           self.bet()
        self.print_number_list()
        self.crack_unknown_modulus();
        print('Modulus '+str(self.modulus))
        print('Multiplier '+str(self.multiplier))
        print('Increment '+str(self.increment))

    def get_next_number(self):
        result = (self.numberList[len(self.numberList)-1] * self.multiplier + self.increment) % self.modulus;
        if(result > 2147483647):
            result = result%2147483647
        return result

    def start(self):
        self.initial_start()
        while(self.money<FINISH_AMOUNT):
            self.bet(number=self.get_next_number(), amount=100);

    def print_number_list(self):
        print(self.numberList)


braker = MakeMeRich()

braker.start()


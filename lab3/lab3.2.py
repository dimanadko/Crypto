import requests
import dateutil.parser
import datetime
import random
import calendar

from numpy import uint32

N = 624;

class MersenneTwister():
    def __init__(self, seed):
        self.index = 0
        self.states = [0]*N
        self.states[0] = uint32(seed)
        for i in range(1, N):
            x = self.states[i-1] ^ (self.states[i-1] >> 30)
            self.states[i] = uint32(
                    ((((x & 0xffff0000) >> 16) * 1812433253) << 16)
                    + ((((x & 0x0000ffff) >>  0) * 1812433253) <<  0)
                    + i)

    @staticmethod
    def from_states(states):
        mt = MersenneTwister(0)
        mt.states = map(MersenneTwister.untemper, states)
        return  mt

    @staticmethod
    def temper(y):
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9d2c5680
        y ^= (y << 15) & 0xefc60000
        y ^= (y >> 18)
        return y

    @staticmethod
    def untemper(y):
        y ^= (y >> 18)
        y ^= (y << 15) & 0xefc60000
        y ^= ((y << 7) & 0x9d2c5680) ^ ((y << 14) & 0x94284000) ^ ((y << 21) & 0x14200000) ^ ((y << 28) & 0x10000000)
        y ^= (y >> 11) ^ (y >> 22)
        return y

    def next(self):
        if (self.index == 0):
          for i in range(N):
            x = uint32((self.states[i] & (1 << 31)) +(self.states[(i + 1) % N] & ((1 << 31) - 1)));
            self.states[i] = (self.states[(i + 397) % N] ^ x >> 1);
            self.states[i] = uint32((self.states[i] ^ 0x9908B0DF) if(x & 1) else self.states[i]);

        value = MersenneTwister.temper(self.states[self.index]);
        self.index = (self.index + 1) % N;

        return value


PLAYER_ID = 221
FINISH_AMOUNT = 1000000





class MakeMeRich():
    def __init__(self):
        """Constructor"""
        self.numberList = []
        self.seed = None
        self.money = 0;

    def create_account(self):
        id = str(input("AccountId: "))
        try:
            r = requests.get('http://95.217.177.249/casino/createacc?id='+id);
            print(r)
            return r.json()['id']
        except requests.exceptions.RequestException as e:
            return self.create_account();

    def bet(self, id, amount=1, mode='Mt', number=1):
        r = requests.get('http://95.217.177.249/casino/play'+mode+'?id='+id+'&bet='+str(amount)+'&number='+str(number)).json()
        print(r)
        self.numberList.append(r['realNumber'])
        if(len(self.numberList)>3):
            self.numberList.pop(0)
        self.money = r['account']['money']
        return r['realNumber'], r['account']['deletionTime'], self.money,

    def initial_start(self, id='1'):
        real_number, del_time, money = self.bet(id=id)
        curr_time = int(dateutil.parser.parse(del_time).timestamp())
        for i in range(-3610, 0):
            generator = MersenneTwister(curr_time+i)
            value = generator.next()
            if(int(value) == real_number):
                print(curr_time+i)
                print('YESSSSSSSSSSSSSSSSSS')
                self.seed = curr_time+i
                break

        generator = MersenneTwister(curr_time + i)
        generator.next()
        while (self.money < FINISH_AMOUNT):
            self.bet(id=id, number=generator.next(), amount=501);

    def start(self):
        id = self.create_account()
        self.initial_start(id)


braker = MakeMeRich()

braker.start()

# print(uint32(3911332162))

# random = Random(datetime.now().second)
# print(random.random())
# print(random.random())

import requests
import json
import math
import functools
from datetime import datetime
import time
import calendar
from mt19937 import Random

from numpy.random import Generator, MT19937, SeedSequence

PLAYER_ID = 221
FINISH_AMOUNT = 1000000





class MakeMeRich():
    def __init__(self):
        """Constructor"""
        self.numberList = []
        self.multiplier = None
        self.modulus = 2**32
        self.increment = None
        self.seed = None
        self.money = 0;

    def create_account(self):
        id = str(input("AccountId"))
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
        return r['realNumber'], r['account']['money'], r['message'],

    def initial_start(self, id='1'):
        # real_number = self.bet(id=id)
        curr_time = calendar.timegm(time.gmtime())
        for i in range(-60, 60):
            sg = SeedSequence(1234)
            rg = [Generator(MT19937(s)) for s in sg.spawn(10)]
            # bit_generator = MT19937(curr_time+i)
            # value = Generator(bit_generator)
            # random = Random(curr_time+i)
            # value = random.random()
            # print(value)
            print(rg)
            # print(bit_generator)
            # if(value == real_number):
            #     print(curr_time+i)
            #     print('YESSSSSSSSSSSSSSSSSS')

        # self.print_number_list()
        # self.crack_unknown_multiplier(self.modulus);
        # print('Modulus '+str(self.modulus))
        # print('Multiplier '+str(self.multiplier))
        # print('Increment '+str(self.increment))

    # def get_next_number(self):
        # result = (self.numberList[len(self.numberList)-1] * self.multiplier + self.increment) % self.modulus;
        # if(result > 2147483647):
        #     result = result%2147483647
        # return result

    def start(self):
        # id = self.create_account()
        self.initial_start()
        # while(self.money<FINISH_AMOUNT):
        #     self.bet(number=self.get_next_number(), amount=300);

    def print_number_list(self):
        print(self.numberList)


braker = MakeMeRich()

braker.start()

# random = Random(datetime.now().second)
# print(random.random())
# print(random.random())

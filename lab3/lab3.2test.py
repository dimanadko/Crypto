import random
import sys

# compatibility
_to_bytes = lambda n, *args, **kwargs: n.to_bytes(*args, **kwargs)
_from_bytes = lambda *args, **kwargs: int.from_bytes(*args, **kwargs)

N = 624  #: 624 values (of 32bit) is just enough to reconstruct the internal state
M = 397  #:
MATRIX_A   = 0x9908b0df  #:
UPPER_MASK = 0x80000000  #:
LOWER_MASK = 0x7fffffff  #:

def tempering(y):
    y ^= (y >> 11)
    y ^= (y <<  7) & 0x9d2c5680
    y ^= (y << 15) & 0xefc60000
    y ^= (y >> 18)
    return y

def untempering(y):
    y ^= (y >> 18)
    y ^= (y << 15) & 0xefc60000
    y ^= ((y <<  7) & 0x9d2c5680) ^ ((y << 14) & 0x94284000) ^ ((y << 21) & 0x14200000) ^ ((y << 28) & 0x10000000)
    y ^= (y >> 11) ^ (y >> 22)
    return y

def generate(mt, kk):
    mag01 = [0x0, MATRIX_A]
    y = (mt[kk] & UPPER_MASK) | (mt[(kk + 1) % N] & LOWER_MASK)
    mt[kk] = mt[(kk + M) % N] ^ (y >> 1) ^ mag01[y & 0x1]

def genrand_int32(mt, mti):
    generate(mt, mti)
    y = mt[mti]
    mti = (mti + 1) % N
    return tempering(y), mti


class MT19937Predictor(random.Random):
    '''
    Usage:
    .. doctest::
        >>> import random
        >>> from mt19937predictor import MT19937Predictor
        >>> predictor = MT19937Predictor()
        >>> for _ in range(624):
        ...     x = random.getrandbits(32)
        ...     predictor.setrandbits(x, 32)
        >>> random.getrandbits(32) == predictor.getrandbits(32)
        True
        >>> random.random() == predictor.random()
        True
        >>> a = list(range(100))
        >>> b = list(range(100))
        >>> random.shuffle(a)
        >>> predictor.shuffle(b)
        >>> a == b
        True
    '''

    def __init__(self):
        self._mt = [ 0 ] * N
        self._mti = 0

    def setrand_int32(self, y):
        '''Feceive the target PRNG's outputs and reconstruct the inner state.
        when 624 consecutive DOWRDs is given, the inner state is uniquely determined.
        '''
        assert 0 <= y < 2 ** 32
        self._mt[self._mti] = untempering(y)
        self._mti = (self._mti + 1) % N

    def genrand_int32(self):
        y, self._mti = genrand_int32(self._mt, self._mti)
        return y


predictor = MT19937Predictor()

import random

from defines import *
from utils import *


def generate_key(step):
    random.seed(KEY)
    key = 0
    for i in range(step):
        key = key ^ random.randint(0xF000, 0xFFFF)
    return key & get_mask(16)


def F(x1, x2, x3, key):
    f1 = left_shift(x1, 9, 16)
    f2 = right_shift(x2, 6, 16)
    f3 = left_shift(x3, 4, 16)
    f4 = right_shift(key, 11, 16) | x2
    return f1 ^ f2 ^ f3 ^ f4


def xor(x, key):
    tmp = x.copy()
    tmp[3] = x[3] ^ F(x[0], x[1], x[2], key)
    return tmp


def cipher_block(msg_block, N=8, debug=False):
    X = gimme_blocks(msg_block)

    for step in range(N):
        key = generate_key(step)

        if debug:
            print(f'in  ({step:02}):  [ {X[0]:04X} , {X[1]:04X} , {X[2]:04X} , {X[3]:04X} ]')

        X_i = xor(X, key)

        if step < N - 1:
            X = rotate(X_i)
        else:
            X = X_i

        if debug:
            print(f'out ({step:02}):  [ {X[0]:04X} , {X[1]:04X} , {X[2]:04X} , {X[3]:04X} ]')

    return restore_from_blocks(X)


def decipher_block(ct_block, N=8, debug=False):
    X = gimme_blocks(ct_block)

    for step in reversed(range(N)):
        key = generate_key(step)

        if debug:
            print(f'in  ({step:02}):  [ {X[0]:04X} , {X[1]:04X} , {X[2]:04X} , {X[3]:04X} ]')

        X_i = xor(X, key)

        if step > 0:
            X = rotate(X_i, -1)
        else:
            X = X_i

        if debug:
            print(f'out ({step:02}):  [ {X[0]:04X} , {X[1]:04X} , {X[2]:04X} , {X[3]:04X} ]')

    return restore_from_blocks(X)


def cipher(msg, N=8, mode='ecb', debug=False):
    x = padding(msg)
    blocks = list(map(''.join, zip(*[iter(x)] * 8)))
    ct = []

    if mode == 'ecb':
        for b in blocks:
            b = str2int(b)
            b = cipher_block(b, N, debug)
            b = int2bytes(b)
            ct.append(b)
        ct = b''.join(ct)
    elif mode == 'cbc':
        blocks_copy = blocks.copy()
        for i in range(len(blocks_copy)):
            blocks_copy[i] = str2int(blocks_copy[i])
        blocks_copy[0] = IV ^ blocks_copy[0]
        blocks_copy[0] = cipher_block(blocks_copy[0], N, debug)
        for i in range(1, len(blocks)):
            blocks_copy[i] = blocks_copy[i] ^ blocks_copy[i - 1]
            blocks_copy[i] = cipher_block(blocks_copy[i], N, debug)
        for i in range(len(blocks_copy)):
            blocks_copy[i] = int2bytes(blocks_copy[i])
            ct.append(blocks_copy[i])
        ct = b''.join(ct)
    elif mode == 'ofb':
        pass


    return ct


def decipher(ct, N=8, mode='ecb', debug=False):
    blocks = chunk(ct)
    msg = []
    ret = ''

    if mode == 'ecb':
        for b in blocks:
            b = bytes2int(b)
            b = decipher_block(b, N, debug)
            b = int2str(b)
            msg.append(b)
        msg = ''.join(msg)
    elif mode == 'cbc':
        blocks_copy = blocks.copy()
        for i in range(len(blocks_copy)):
            blocks_copy[i] = bytes2int(blocks_copy[i])
        blocks_copy[0] = decipher_block(blocks_copy[0], N, debug)
        blocks_copy[0] = IV ^ blocks_copy[0]
        for i in range(1, len(blocks)):
            blocks_copy[i] = decipher_block(blocks_copy[i], N, debug)
            blocks_copy[i] = blocks_copy[i] ^ bytes2int(blocks[i - 1])
        for i in range(len(blocks_copy)):
            blocks_copy[i] = int2str(blocks_copy[i])
            msg.append(blocks_copy[i])
        msg = ''.join(msg)
    elif mode == 'ofb':
        pass

    msg = unpadding(msg)
    return msg


def main():
    msg = input('Enter message:')

    print(f'msg: {msg}')
    print(f'     {str2int(msg):X}')

    ct = cipher(msg, 16, 'cbc')
    print(f'ct:  {bytes2int(ct):X}')

    dt = decipher(ct, 16, 'cbc')
    print(f'dc:  {dt}')
    print(f'     {str2int(dt):X}')


if __name__ == '__main__':
    main()


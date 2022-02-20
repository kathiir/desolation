from defines import *

def get_mask(bit):
    mask = 0
    for i in range(bit):
        mask = mask << 1 | 0x1
    return mask


def right_shift(x, shift_value, size):
    shift_value = shift_value % (size + 1)
    return ((x >> shift_value) | (x << (size - shift_value))) & get_mask(size)


def left_shift(x, shift_value, size):
    shift_value = shift_value % (size + 1)
    return ((x << shift_value) | (x >> (size - shift_value))) & get_mask(size)


def rotate(x, step=1):
    if len(x) == 0:
        return x
    step = step % len(x)
    return x[step:] + x[:step]


def gimme_blocks(block):
    x = []
    for i in range(NUMBER_OF_BLOCKS):
        x.append((block >> ((NUMBER_OF_BLOCKS - 1 - i) * SUB_BLOCK_SIZE)) & get_mask(SUB_BLOCK_SIZE))
    return x


def restore_from_blocks(x):
    y = 0
    for i in range(NUMBER_OF_BLOCKS):
        y |= x[i] << ((NUMBER_OF_BLOCKS - 1 - i) * SUB_BLOCK_SIZE)
    return y


def chunk(b_string):
    chunk_size = 8
    num_of_chunks = len(b_string) // 8
    chunks = []
    for i in range(num_of_chunks):
        chunks.append(b_string[i * chunk_size: (i + 1) * chunk_size])
    return chunks


def padding(message):
    pad_size = (8 - len(message) % 8) % 8 + 8
    pad_char = chr(pad_size * 8)
    return message + pad_char * pad_size


def unpadding(padded_text):
    pad_char = padded_text[len(padded_text) - 1]
    pad_size = ord(pad_char) // 8
    return padded_text[:-pad_size]


def str2int(string):
    return int.from_bytes(string.encode('utf-8'), byteorder='big')


def bytes2int(bstring):
    return int.from_bytes(bstring, byteorder='big')


def int2str(num):
    return int.to_bytes(num, length=8, byteorder='big').decode('utf-8')


def int2bytes(num):
    return int.to_bytes(num, length=8, byteorder='big')

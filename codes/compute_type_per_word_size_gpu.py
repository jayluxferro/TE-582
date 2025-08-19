#!/usr/bin/env python3


from time import time
import mlx.core as mx


word_size = int(input("Enter word size in bits (e.g., 8, 16, 32, 64): "))

start_time = time()
for i in mx.arange(0, 2**word_size):
    print(bin(i.item())[2:].zfill(word_size))

end_time = time()

print("Time taken to compute 2^%d: %.6f seconds\n" % (word_size, end_time - start_time))

#!/usr/bin/env python3
""" Main file to test all tasks: store, get, count_calls, call_history, replay """

from exercise import Cache, replay

# Create a new cache instance (flushes Redis)
cache = Cache()

print("\n--- Task 0 & 1: store() and get() ---")

# Test storing and retrieving different data types
key1 = cache.store(b"hello")
key2 = cache.store("world")
key3 = cache.store(123)
key4 = cache.store(45.67)

print("Raw get (bytes):", cache.get(key1))       # b'hello'
print("get_str():", cache.get_str(key2))          # 'world'
print("get_int():", cache.get_int(key3))          # 123
print("Raw get (float):", cache.get(key4))        # b'45.67'

print("\n--- Task 2: count_calls ---")

# Call store multiple times to increase call count
cache.store(b"first")
cache.store(b"second")

# Get how many times 'store' was called
calls = cache.get(cache.store.__qualname__)
print("Cache.store was called:", calls.decode() if calls else "0", "times")

print("\n--- Task 3: call_history ---")

# Manually inspect the inputs and outputs stored in Redis
inputs = cache._redis.lrange(f"{cache.store.__qualname__}:inputs", 0, -1)
outputs = cache._redis.lrange(f"{cache.store.__qualname__}:outputs", 0, -1)

print("Stored inputs:")
for i in inputs:
    print("  ", i.decode())

print("Stored outputs:")
for o in outputs:
    print("  ", o.decode())

print("\n--- Task 4: replay ---")

# Show full function call history
replay(cache.store)

#!/usr/bin/env python
"""
Generate an ECDSA keypair and Bitcoin-compatible payment address.
Requires Brian Warner's excellent python-ecdsa library.

http://github.com/aristus/bitcoin-printer
"""
from ecdsa.ecdsa import Public_key, int_to_string
from ecdsa.ellipticcurve import CurveFp, Point
from binascii import hexlify
import hashlib
ripehash = hashlib.new('ripemd160')

# ***WARNING*** This is possibly insecure! ***WARNING***
from random import SystemRandom
randrange = SystemRandom().randrange

## Bitcoin has an adorable encoding scheme that includes numbers and letters
## but excludes letters which look like numbers, eg "l" and "O"
__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)
def b58encode(v):
  long_value = 0L
  for (i, c) in enumerate(v[::-1]):
    long_value += (256**i) * ord(c)
  result = ''
  while long_value >= __b58base:
    div, mod = divmod(long_value, __b58base)
    result = __b58chars[mod] + result
    long_value = div
  result = __b58chars[long_value] + result
  nPad = 0
  for c in v:
    if c == '\0': nPad += 1
    else: break
  return (__b58chars[0]*nPad) + result


def generate_btc_address():
    # secp256k1, not included in stock ecdsa
    _p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2FL
    _r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141L
    _b = 0x0000000000000000000000000000000000000000000000000000000000000007L
    _a = 0x0000000000000000000000000000000000000000000000000000000000000000L
    _Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798L
    _Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8L
    curve_256 = CurveFp(_p, _a, _b)
    generator = Point(curve_256, _Gx, _Gy, _r)

    secret = randrange(1, generator.order())
    pubkey = Public_key(generator, generator * secret)
    step1 = '\x04' + int_to_string(pubkey.point.x()) + \
        int_to_string(pubkey.point.y())
    step2 = hashlib.sha256(step1).digest()
    ripehash.update(step2)
    step4 = '\x00' + ripehash.digest()
    step5 = hashlib.sha256(step4).digest()
    step6 = hashlib.sha256(step5).digest()
    chksum = step6[:4]
    addr = step4 + chksum
    addr_58 = b58encode(addr)
    return (
        hex(secret)[2:-1],
        hexlify(step1),
        hexlify(addr),
        addr_58
    )

if __name__ == '__main__':
    secret, pubkey, addr, addr_58 = generate_btc_address()
    print 'secret: ', secret
    print 'pubkey: ', pubkey
    print 'address:', addr
    print 'addr_58:', addr_58


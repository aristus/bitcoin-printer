#!/usr/bin/env python

"""
Generate images for a "paper bitcoin"

http://github.com/aristus/bitcoin-printer
"""

import sys
from generate_keypair import generate_btc_address
import qrcode
from PIL import ImageFont, ImageDraw, Image

amount = '0.001'
if len(sys.argv) > 1:
    amount = '%0.3f' % float(sys.argv[1])
amount += " BTC"

typeface = 'Arial Rounded Bold.ttf'
denomination = ImageFont.truetype(typeface, 200)
address = ImageFont.truetype(typeface, 100)
secret, pubkey, addr, addr_58 = generate_btc_address()
secreta = secret[:32]
secretb = secret[32:]

#addr_58 = '1SaMpLErqTBGZu3cUmkCJvmKi4zA3Sp38U'
#secreta = 'http://www.youtube.com/watch?v=oHg5SJYRHA0'
#secretb = 'http://www.youtube.com/watch?v=oHg5SJYRHA0'

## An uninteresting spooge of code. Given a string, generates
## a QR code image object, rotates and resizes it, then
## makes the white bits transparent.
def rotated_qr(s):
    derp = qrcode.make(s)
    i = derp._img.convert('RGBA')
    i = i.rotate(315, expand=1)
    i = i.resize((1100, 1100))
    fff = Image.new('RGBA', i.size, (255,255,255,255))
    i = Image.composite(i, fff, i)
    dataz = i.getdata()
    new_data = []
    for item in dataz:
      if item[0] == 255 and item[1] == 255 and item[2] == 255:
        new_data.append((255, 255, 255, 0))
      else:
        new_data.append(item)
    i.putdata(new_data)
    return i


front = Image.open('template-front.png')
draw = ImageDraw.Draw(front)

## bottom left
draw.text((390, 2075), amount, font=denomination, fill=000)

## top right
draw.text((3740, 430), amount, font=denomination, fill=000)

## address
draw.text((550, 600), addr_58[:18], font=address, fill=000)
draw.text((550, 700), addr_58[18:], font=address, fill=000)

# QRCODEZZZ
addrq = rotated_qr(addr_58)
front.paste(addrq, (520, 830), addrq)
priva = rotated_qr(secreta)
front.paste(priva, (3450, 830), priva)

# write it
front.save(addr_58 + ".front.png", "PNG")

## Now the back.
back = Image.open('template-back.png')
draw = ImageDraw.Draw(back)
draw.text((390, 2220), amount, font=denomination, fill=000)
draw.text((1500, 2280), addr_58, font=address, fill=000)

privb = rotated_qr(secretb)
back.paste(privb, (3700, 1100), privb)

back.save(addr_58 + ".back.png", "PNG")

print "Generated images for", addr_58

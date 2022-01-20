#!/bin/python3

import sys
import os
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import getopt
import binascii

class JencOptions:
    def __init__(self, is_encrypting = True, 
                        is_password = False,
                        is_verbose = False,
                        is_encoding = True,
                        is_decoding = True,
                        is_file = False,
                        is_file_binary = False):
        self.is_encrypting = is_encrypting
        self.is_password = is_password 
        self.is_verbose = is_verbose  
        self.is_encoding = is_encoding 
        self.is_decoding = is_decoding 
        self.is_file = is_file
        self.is_file_binary = is_file_binary

def main(argv):
    options = JencOptions()

    # check arguments
    try:
        opts, args = getopt.getopt(argv,"hvedp:f:")
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
        if (opt == "-f"):
            options.is_file = True
            options.is_encoding = False

            try:
                file_name = str(arg)
            except ValueError: # error if user didn't pass a index 'n'
                print("-f flag should follow path to the file")
                sys.exit(2)

            if (is_file_binary(file_name)):
                options.is_decoding = False
                options.is_file_binary = True

    if (not options.is_password): # end program if there was no -p flag
        help_options()
        sys.exit(3)

    if (not options.is_file):
        user_input = "".join(sys.stdin.readlines()) # get user input
    key = password_to_key(password) # create AES key from user password
    if (options.is_encrypting):
        if (options.is_file):
            encrypt_file(key, file_name, options)
        else :
            print(encrypt(key, user_input, options)) # print encrypted text
    else:
        if (options.is_file):
            decrypt_file(key, file_name, options)
        else:
            print(decrypt(key, user_input, options), end="") # print decrypted text

def help_options():
    print("-h # print this help menu")
    print("-e # encrypt")
    print("-d # decrypt")
    print("-p <password> # password to encrypt/decrypt; you have to use this flag")
    print("-f <path_to_the_file> # file to encrypt/decrypt")
    print("-v # verbose mode")

def is_file_binary(file_name):
    try:
        with open(file_name, 'tr') as f:  # try open file in text mode
            f.read()
            return False
    except:  # if fail then file is non-text (binary)
        return True

def password_to_key(password):
    return SHA256.new(str(password).encode("utf-8")).digest()

def encrypt(key, source, options=None):
    if (options and options.is_encoding):
        source = source.encode("utf-8") # convert string to bytes
    IV = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size # calculate padding
    source += bytes([padding]) * padding
    data = IV + encryptor.encrypt(source) # store the IV at the beginning and encrypt

    return data if (options and not options.is_decoding) else base64.b64encode(data).decode("latin-1")

def encrypt_file(key, file_name, options=None):
    if (not os.path.isfile(file_name)):
        sys.stderr.write("file doesn't exist\n")
    else:
        file_data = None
        with open(file_name, "rb") as f:
            file_data = f.read()

        encrypted_data = encrypt(key, file_data,options)

        file_mode = "wb" if (options and options.is_file_binary) else "w"

        with open(file_name, file_mode) as f:
            f.write(encrypted_data)

def decrypt(key, source, options=None):
    try:
        if (options and options.is_decoding):
            source = base64.b64decode(source.encode("latin-1"))
        IV = source[:AES.block_size]
        decryptor = AES.new(key, AES.MODE_CBC, IV)
        data = decryptor.decrypt(source[AES.block_size:]) # decrypt
    except binascii.Error as e:
        if (options and options.is_verbose):
            print(e)
        sys.stderr.write("data wasn't encrypted\n")
        return ""
    except ValueError as e:
        if (options and options.is_verbose):
            print(e)
        sys.stderr.write("data wasn't encrypted\n")
        return ""

    padding = data[-1]

    if data[-padding:] != bytes([padding]) * padding:
        sys.stderr.write("wrong password\n")
        return ""

    return (data[:-padding]).decode("utf-8") if (options and options.is_decoding) else data[:-padding] # remove the padding and decode into utf-8 format

def decrypt_file(key, file_name, options=None):
    if (not os.path.isfile(file_name)):
        sys.stderr.write("file doesn't exist\n")
    else:
        file_data = None
        file_mode = "rb" if (options and options.is_file_binary) else "r"
        with open(file_name, file_mode) as f:
            file_data = f.read()

        decrypted_data = decrypt(key, file_data,options)

        if (decrypted_data != ""):
            file_mode = "wb" if (options and options.is_file_binary) else "w"

            with open(file_name, file_mode) as f:
                f.write(decrypted_data)

if (__name__ == "__main__"):
    main(sys.argv[1:])

# Script hash_func to be used in main.da and client.da
#
import hashlib
import zlib
import configparser


def hash_func(name, m):
    return hash_sha512(name, m)


def hash_sha1(name, m):
    return int(hashlib.sha1(bytes(name.encode('utf-8'))).hexdigest(), 16) % 2 ** m


def hash_sha512(name, m):
    return int(hashlib.sha3_512(bytes(name.encode('utf-8'))).hexdigest(), 16) % 2 ** m


def hash_sha256(name, m):
    return int(hashlib.sha3_256(bytes(name.encode('utf-8'))).hexdigest(), 16) % 2 ** m


def hash_sha224(name, m):
    return int(hashlib.sha3_224(bytes(name.encode('utf-8'))).hexdigest(), 16) % 2 ** m


def hash_sha384(name, m):
    return int(hashlib.sha3_384(bytes(name.encode('utf-8')))) % 2 ** m


def adler32(name, m):
    return int(zlib.adler32(bytes(name.encode('utf-8')))) % 2 ** m


def crc32(name, m):
    return int(zlib.crc32(bytes(name.encode('utf-8')))) % 2 ** m

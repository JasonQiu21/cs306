# I pledge my honor that I have abided by the Stevens Honor System.

# Jason Qiu
# 2022-11-03
import hashlib
import sys
import random
import secrets
import copy

def gen_key():
    sk = [[],[]]
    for i in range(2):
        for j in range(256):
            sk[i].append(secrets.token_bytes(32))
    pk = [[],[]]
    for i in range(2):
        for j in sk[i]:
            pk[i].append(hashlib.sha256(str(j).encode('utf-8')).hexdigest())
    return sk, pk

def server_gen_key(n):
    sk, pk = gen_key()
    keys = [copy.deepcopy(pk)]
    for i in range(n):
        for i in range(2):
            for j in range(len(pk[i])):
                pk[i][j] = hashlib.sha256(pk[i][j].encode('utf-8')).hexdigest()
        keys.append(copy.deepcopy(pk))
    return keys

def sign(d, sk):
    digest = bin(int(d, 16))[2:]
    signature = []
    for i in range(len(digest)):
        signature.append(sk[int(digest[i])][i])
    return signature

def verify(d, ds, pk):
    digest = bin(int(d, 16))[2:]
    for i in range(len(ds)):
        assert hashlib.sha256(str(ds[i]).encode('utf-8')).hexdigest() == pk[int(digest[i])][i], f"Discrepancy between index {i} in public key and received signature"

if __name__ == '__main__':
    # Keygen
    print('Generating Keys...')
    sk, pk = gen_key()
    print("Done.")

    message = "The treasure is located in Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch."
    d = hashlib.sha256(message.encode('utf-8')).hexdigest()
    print(f"Message = {message}\nDigest = {d}")

    ds = sign(d, sk)

    print("--------------------------------------------------Valid Message and Signature Verification--------------------------------------------------")
    print(f"Send message '{message}' and signature.\nReciever: verifying...")
    verify(d, ds, pk)
    print(f"No errors in verify. Message is valid.")

    print("--------------------------------------------------Altered Message Verification--------------------------------------------------")
    altered_message = "The treasure is located in Lake Chargoggagoggmanchauggagoggchaubunagungamaugg."
    altered_d = hashlib.sha256(altered_message.encode('utf-8')).hexdigest()
    print(f"Send message altered message '{altered_message}' and signature.\nReciever: verifying...")
    try:
        verify(altered_d, ds, pk)
        raise Exception("Error: Expected error in verify, none received")
    except AssertionError as e:
        print(f"Received error: {e}. Reject message")

    print("--------------------------------------------------Altered Signature Verification--------------------------------------------------")
    altered_ds = ds[:-1] + (['0' if ds[-1] != '0' else '1'])
    print(f"Send message '{message}' and altered signature.\nReciever: verifying...")
    try:
        verify(d, altered_ds, pk)
        raise Exception("Error: Expected error in verify, none received")
    except AssertionError as e:
        print(f"Received error: {e}. Reject message")


    print("--------------------------------------------------Client/Server Key Exchange--------------------------------------------------")
    n = 64
    server_keys = server_gen_key(n)
    server_key = copy.deepcopy(server_keys[n])
    print(f"Server: sends H^{n}(K) .. H(k) to Client")
    
    for i in range(n-1, -1, -1):
        print(f"Client sends H^{i+1}(K).")
        key = copy.deepcopy(server_keys[i])
        for k in range(len(key)):
            for j in range(len(key[k])):
                if hashlib.sha256(key[k][j].encode('utf-8')).hexdigest() != server_key[k][j]:
                    raise Exception(f"Discrepancy on key[{k}][{j}]. Authentication failed.")
        print(f"Authenticated.")
        server_key = copy.deepcopy(server_keys[i])

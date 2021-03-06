# import libraries
import hashlib
import binascii
import datetime
import collections

# following imports are required by PKI
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class Client:
    def __init__(self):
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')


# Rodrigo = Client()
# print(Rodrigo.identity)  # Public Key

class Transaction:
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()

    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity
        return collections.OrderedDict(
            {'sender': identity, 'recipient': self.recipient, 'value': self.value, 'time': self.time})

    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


Renata = Client()
Pablo = Client()
Rodrigo = Client()
Audrey = Client()
Marshall = Client()


def display_transaction(transaction):
    # for transaction in transactions:
    dict = transaction.to_dict()
    print("sender: " + dict['sender'])
    print('-----')
    print("recipient: " + dict['recipient'])
    print('-----')
    print("value: " + str(dict['value']))
    print('-----')
    print("time: " + str(dict['time']))
    print('-----')


transactions = []

t0 = Transaction("Genesis", Pablo.identity, 500)
# t0.sign_transaction()
transactions.append(t0)

t1 = Transaction(Pablo, Rodrigo.identity, 100)
t1.sign_transaction()
transactions.append(t1)

t1 = Transaction(Pablo, Rodrigo.identity, 100)
t1.sign_transaction()
transactions.append(t1)

t2 = Transaction(Rodrigo, Audrey.identity, 10)
t2.sign_transaction()
transactions.append(t2)

t3 = Transaction(Rodrigo, Marshall.identity, 10)
t3.sign_transaction()
transactions.append(t3)

t4 = Transaction(Marshall, Audrey.identity, 5)
t4.sign_transaction()
transactions.append(t4)


# for transaction in transactions:
#     display_transaction(transaction)


class Block:
    def __init__(self):
        self.verified_transactions = []
        self.previous_block_hash = ""
        self.Nonce = ""


last_block_hash = ""

block0 = Block()
block0.previous_block_hash = None
Nonce = None

block0.verified_transactions.append(t0)
block0.verified_transactions.append(t1)
digest = hash(block0)
last_block_hash = digest

TPCoins = []


def dump_blockchain(self):
    print("Number of blocks in the chain: " + str(len(self)))
    for x in range(len(TPCoins)):
        block_temp = TPCoins[x]
        print("block # " + str(x))
    for transaction in block_temp.verified_transactions:
        display_transaction(transaction)
        print('---------------------------------\n')
    print('=====================================')


TPCoins.append(block0)
dump_blockchain(TPCoins)


def sha256(message):
    return hashlib.sha256(message.encode('ascii')).hexdigest()


def mine(message, difficulty=1):
    assert difficulty >= 1
    prefix = '1' * difficulty
    i = 0
    while True:
        i += 1
        digest = sha256(str(message) + str(i))
        if digest.startswith(prefix):
            print("after " + str(i) + " iterations found nonce: " + digest)
            return i, digest


print(mine("Rodrigo", 6))
# 11111187cfc9ff59ab4564de7f9c1d30eaa92b1b16c99537bc96bd90126dbb27
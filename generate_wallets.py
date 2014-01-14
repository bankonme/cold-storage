#!/usr/bin/env/python

# Generate bitcoin private keys on an airgapped machine
# See blog post before using

import csv
from datetime import datetime

# Download pycoin (https://github.com/richardkiss/pycoin)
# and put this file in the root directory so that these imports work
from pycoin.wallet import Wallet
from pycoin.encoding import is_valid_wif

# Set the number of keys you want to generate here:
NUM_KEYS_TO_GENERATE = 100000

def devrandom_entropy():
    return open("/dev/random", "rb").read(64)

def generate_random_wallet():
    entropy = bytearray(devrandom_entropy())
    return Wallet.from_master_secret(bytes(entropy), is_test=False)

if __name__ == '__main__':
    START_TIME = datetime.now()
    FILE_NAME = '/media/wipeout/btc_keys_%s.csv' % START_TIME.strftime("%Y%m%d_%H%M")
    HEADERS = ['born_at', 'wif', 'public_bitcoin_address']

    all_wifs = set()
    all_public_addresses = set()

    print 'Starting wallet generation at %s...' % START_TIME
    print 'Saving results to %s...' % FILE_NAME

    with open(FILE_NAME, 'w') as f:
        myWriter = csv.DictWriter(f, HEADERS)

        # For some reason this doesn't work on tails' python installation:
        # myWriter.writeheader()

        # Hack to write header row anyway:
        HEADER_DICT = {}
        for header in HEADERS:
            HEADER_DICT[header]=header
        myWriter.writerow(HEADER_DICT)

        for key_cnt in range(NUM_KEYS_TO_GENERATE):
            wallet = generate_random_wallet()
            public_address = wallet.bitcoin_address()
            wif = wallet.wif()
            wallet_dict = {
                'born_at': datetime.now(),
                'wif': wif,
                'public_bitcoin_address': public_address,
                }
            myWriter.writerow(wallet_dict)

            # weak safety chcecks
            assert is_valid_wif(wif)
            assert wif not in all_wifs
            assert public_address not in all_public_addresses

            # add wallet to set
            all_wifs.add(wif)
            all_public_addresses.add(public_address)

            # print out progress
            if key_cnt % 500 == 0:
                print key_cnt, datetime.now()

    END_TIME = datetime.now()
    print 'Finished generating %s private keys at %s (%s run time)' % (key_cnt+1, END_TIME, END_TIME-START_TIME)

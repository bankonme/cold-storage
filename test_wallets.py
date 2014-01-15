#!/usr/bin/env/python

# Test bitcoin private keys on an airgapped machine
# See blog post before using

import csv
from subprocess import check_output

# update this with your filename:
FILE_NAME = '/media/wipeout/btc_keys_20140113_2058.csv'
# depending on your installation, you may have to call `bitcoin-tool` with full path
SHELL_STRING = '''bitcoin-tool \
                    --input-type private-key \
                    --input-format base58check \
                    --input %s \
                    --output-type address \
                    --output-format base58check'''

def get_address_from_wif(wif):
    return check_output(SHELL_STRING % wif, shell=True).strip()

print 'Checking all wallets in %s...' % FILE_NAME

with open(FILE_NAME, 'r') as f:
    for cnt, row in enumerate(csv.DictReader(f)):
        if cnt % 500 == 0:
            print 'Checking wallet #%s...' % cnt
        assert row['public_bitcoin_address'] == get_address_from_wif(row['wif'])

print 'All %s wallets were tested and are valid!' % cnt+1

#!/usr/bin/env/python

# A script to verify that ssss-split shares will in fact recombine

import pexpect
from itertools import combinations

# Change these values with your own:
SECRET = 'the quick brown fox jumped over the lazy dog'
SHARES = """
01-bd20b94290ed28703750c00949f007a3097af1b0f60440e7362998e5406ff624a48eff8662c4ef4989b9b95c
02-03475b94cb4311334f9e234feefc0de14327b273c37171d8970d05fd1467869b2a0812d11401276c44120304
03-7e5a07d5be81c2b1319cde41f64faa9ca50fdf42174c8d0ace442092318a438dbaeaa85882453a7d3d3053b9
04-2d675127b0b23aa6f628edf2a493e49b7a54b1fa2eaaaf3ca6428e4a70e6b9f9c6eea2ac56c6aae58e558cd1
05-e58d51f58d962c90b35b0efc20d6d376c0b17094b71904e076c5e781543dd3f29cea6050348046cc3676dc6f
06-4ef788392fea1be5f7fe75eaa1f9cd9d6d517e180964e4edc98a1d8ff3e0ce58a1ddb727f03e8c85863e5e17
07-1eaacc0972ebcdf0141ec54f13d97618bafaec4fe2522c5143de490c2ab996836fea93e41ddc6616818bc158
08-80892e08c8720ff33cbddcfbac76912278079654467803bf41470b323ed90f5484b09fdbbac69f963afd7038
09-a0216358afc955da346107ef3205cbf1de7a6dd2f796cc99a17438d71a9f105b80df1b99603e813af99e3963
10-94fa588863adb71d08e2e722f7ca30ba8979f9486f321719f23233cfa6fccf3bae05ae2f2ef373c3c6fb6bef
11-2ce5513a64332d17a6ad6f9d5fdce601424a51f7ac59bb5f48d23d627f38e2e43e59cc527baf6bd5ba0eed45
""".strip().split()
THRESHOLD = 6

def test_shares(sharegroup, secret):
    child = pexpect.spawn('ssss-combine -t %d' % len(sharegroup), timeout=3)
    for share in sharegroup:
        print 'Share to send:', share
        child.sendline(share)
    response = child.read()

    result = [x for x in response.split('\n') if 'Resulting secret: ' in x][0].split(':')[1].strip()

    if result == secret:
        return True
    return False

if __name__ == '__main__':
    sharegroups_to_test = list(combinations(SHARES, THRESHOLD))

    print 'Testing %s sharegroups...' % len(sharegroups_to_test)

    for cnt, sharegroup in enumerate(sharegroups_to_test):
        assert test_shares(sharegroup, SECRET)
        print '%s PASSED' % (cnt+1)

# pip3 install requests - maybe needed, if this is used per terminal

import requests
import hashlib
import sys
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char  # first 5 of hash of ..
    res = requests.get(url)
    # print(res)  # RESPONSE [200]
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check API and try again.')
    return res

def get_pwd_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        # print(h, count)
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_5_char, tail = sha1_password[:5], sha1_password[5:],
    pwned_response = request_api_data(first_5_char)
    print(first_5_char, tail)
    # print(pwned_response)
    return get_pwd_leaks_count(pwned_response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times .. pls change your password.')
        else:
            print(f'{password} was NOT found. Lucky bastard!')
    return 'done!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

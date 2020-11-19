import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char

    res = requests.get(url)

    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching {res.status_code}. Server down, check api and try again')
    return res


def get_password_leak_count(hashes, hash_to_check):

    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count

    return 0


def pwned_api_check(password):
    value = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = value[:5], value[5:]

    response = request_api_data(first5_char)
    # print(first5_char, tail)
    return get_password_leak_count(response, tail)


def main(argv):

    count = pwned_api_check(argv)
    if count:
        print(
            f'{argv} was found {count} times. You should probably change it')
    else:
        print(f'{argv} was Not found. Feel free to use it.')

    # for password in argv:
    #     count = pwned_api_check(password)
    #     if count:
    #         print(
    #             f'{password} was found {count} times. You should probably change it')
    #     else:
    #         print(f'{password} was Not found. Feel free to use it.')

    return 'Done Captain'


if __name__ == '__main__':

    # sys.exit(main(sys.argv[1:]))

    password = input('Your password: ')
    sys.exit(main(password))

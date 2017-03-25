#! /usr/local/bin Pythono3

from iitable import fetch_iitable


def iitable_to_file():
    iitable = fetch_iitable()

    with open('iitable.txt', 'w') as f:
        for word, chain in iitable.items():
            f.write(str(chain) + '\n')


if __name__ == '__main__':
    iitable_to_file()

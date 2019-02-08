# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import fileinput


def replace_images(dir, origin, new):
    url_pattern = re.compile('.+(' + origin.replace('.', '\.') +').+')

    for filename in os.listdir(dir):
        for line in fileinput.input(dir + filename, inplace=True):
            print(line.replace(origin, new), end='')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='This script replaces images\'bed')
    parser.add_argument('-d', '--directory', help='Experiment directory', required=True)
    parser.add_argument('-o', '--origin', help='Origin image-bed', required=True)
    parser.add_argument('-n', '--new', help='New iamge-bed', required=False)
    args = parser.parse_args()
    replace_images(args.directory, args.origin, args.new)

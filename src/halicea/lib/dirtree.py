#!/usr/bin/env python
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.#! /usr/bin/env python

# tree.py
#
# Written by Doug Dahms
#
# Prints the tree structure for the path specified on the command line

from os import listdir, sep
from os.path import abspath, basename, isdir
from sys import argv

def tree(dir, padding, print_files=False, depth=3):
    print padding[:-1] + '+-' + basename(abspath(dir)) + '/'
    padding = padding + ' '
    files = []
    if print_files:
        files = listdir(dir)
    else:
        files = [x for x in listdir(dir) if isdir(dir + sep + x)]
    count = 0
    if depth!=0:
        for file in files:
            count += 1
            print padding + '|'
            path = dir + sep + file
            if isdir(path):
                if count == len(files):
                    tree(path, padding + ' ', print_files, depth-1)
                else:
                    tree(path, padding + '|', print_files, depth-1)
            else:
                print padding + '+-' + file

def usage():
    return '''Usage: %s [-f] <PATH>
Print tree structure of path specified.
Options:
-f      Print files as well as directories
PATH    Path to process''' % basename(argv[0])

def main():
    if len(argv) == 1:
        print usage()
    elif len(argv) == 2:
        # print just directories
        path = argv[1]
        if isdir(path):
            tree(path, ' ')
        else:
            print 'ERROR: \'' + path + '\' is not a directory'
    elif len(argv) == 3 and argv[1] == '-f':
        # print directories and files
        path = argv[2]
        if isdir(path):
            tree(path, ' ', True)
        else:
            print 'ERROR: \'' + path + '\' is not a directory'
    else:
        print usage()

if __name__ == '__main__':
    main()

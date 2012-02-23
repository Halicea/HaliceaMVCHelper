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
#along with this program.  If not, see <http://www.gnu.org/licenses/>.'''Module with methods for File IO operations'''
from consoleHelpers import ask
import os, shutil

def copy_directory(source, target, ignoreDirs=[], ignoreFiles=[]):
    ignoreDirsSet =set(ignoreDirs)
    if not os.path.exists(target):
        os.mkdir(target)
    for root, dirs, files in os.walk(source):
        ignoreCurrentDirs = list(ignoreDirsSet.intersection(set(dirs)))

        for t in ignoreCurrentDirs:
            #print 'Ignoring', t
            dirs.remove(t)  # don't visit .svn directories
        for file in files:
            if os.path.splitext(file)[-1] in ignoreFiles:
                #print 'skipped', file
                continue
            from_ = os.path.join(root, file)
            to_ = from_.replace(source, target, 1)
            to_directory = os.path.split(to_)[0]
            if not os.path.exists(to_directory):
                os.makedirs(to_directory)
            shutil.copyfile(from_, to_)

def saveTextToFile(txt, skipAsk=False, skipOverwrite=False):
    save = skipAsk and ask('Save to File?')
    if save:
        filePath = raw_input('Enter the Path>')
        if os.path.exists(filePath):
            again = True
            while again:
                again = False
                p = skipOverwrite and ask('File already Exists, (o)verwrite, (a)ppend, (p)repend or (c)ancel?>',
                                          {'o':'o', 'a':'a','c':'c','p':'p',})
                if p=='o' or p==False:
                    f = open(filePath, 'w'); f.write(txt); f.close()
                elif p=='a':
                    f = open(filePath, 'a'); f.write(txt); f.close()
                elif p=='p':
                    f = open(filePath, 'r'); txt = txt+'\n'+f.read(); f.close()
                    f = open(filePath, 'w'); f.write(txt); f.close()
                elif p == 'c':
                    pass
                else:
                    print 'Not Valid Command, Options: o, a, p, c lowercase only!'
                    again = True

                if not again and p!='c':
                    print 'File saved at \"%s\"!'%filePath
        else:
            f = open(p, 'w'); f.write(txt); f.close()

def getTextFromPath(filePath):
    templ = ''
    if filePath[-1]==']' and filePath.rindex('[')>0:
        fn= filePath
        lindex = int(fn[fn.rindex('[')+1:fn.rindex(':')])
        rindex = int(fn[fn.rindex(':')+1:-1])
        f = open(filePath[:filePath.rindex('[')], 'r')
        templ = ''.join(f.readlines()[lindex:rindex])
        f.close()
    else:
        templ = open(filePath,'r').read()
    return templ

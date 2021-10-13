from posixpath import splitext
import zipfile
import rarfile
from os import listdir, remove
from os.path import isfile, join, splitext

def isZipFile(path):
    return zipfile.is_zipfile(path)

def isRarFile(path):
    return rarfile.is_rarfile(path)

def without_extension(dir):
    return splitext(dir)[0]

def remove_file(dir):
    remove(dir)

def unzip(from_dir, to):
    with zipfile.ZipFile(from_dir, 'r') as zip_ref:
        zip_ref.extractall(to)
        onlyfiles = [f for f in listdir(to) if isfile(join(to, f))]
        for f in onlyfiles:
            try:
                unzip(to + '/' + f, without_extension(to + '/' + f))
                remove_file(to + '/' + f)
            except Exception as e:
                print(f + " is not a zip folder")

def unrar(from_dir, to):
    with rarfile.RarFile(from_dir, 'r') as rar_ref:
        rar_ref.extractall(to)
        onlyfiles = [f for f in listdir(to) if isfile(join(to, f))]
        for f in onlyfiles:
            try:
                unrar(to + '/' + f, without_extension(to + '/' + f))
                remove_file(to + '/' + f)
            except Exception as e:
                print(f + " is not a rar folder")

'''

from unarchivers import unrar, unzip

print('Enter the directory of the file archive: ', end='')
from_dir = input()
try:
    unrar(from_dir, '')
except Exception:
    pass


try:
    unzip(from_dir, '')
except Exception:
    pass

'''

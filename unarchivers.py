from posixpath import splitext
import zipfile
import rarfile
from os import listdir, remove
from os.path import isfile, join, splitext

def is_zip_file(path):
    return zipfile.is_zipfile(path)

def is_rar_file(path):
    return rarfile.is_rarfile(path)

def without_extension(dir):
    return splitext(dir)[0]

def remove_file(dir):
    remove(dir)

def unzip(from_dir, to):
    with zipfile.ZipFile(from_dir, 'r') as zip_ref:
        zip_ref.extractall(to)

    # go through all files
    onlyfiles = [f for f in listdir(to) if isfile(join(to, f))]
    for f in onlyfiles:
        try:
            unzip(to + '/' + f, without_extension(to + '/' + f))
            remove_file(from_dir)
        except Exception:
            print(f + ' is not a zip folder')

    # go through all folders
    onlyfolders = [f for f in listdir(to) if not isfile(join(to, f))]
    for f in onlyfolders:
        unzip_folder(to + '/' + f)

def unzip_folder(path):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        for f in onlyfiles:
            try:
                unzip(path + '/' + f, without_extension(path + '/' + f))
                remove_file(path + '/' + f)

            except Exception:
                print(f + ' is not a zip folder')

        # go through all folders
        onlyfolders = [f for f in listdir(path) if not isfile(join(path, f))]
        for f in onlyfolders:
            unzip_folder(path + '/' + f)  


def unrar(from_dir, to):
    with rarfile.RarFile(from_dir, 'r') as rar_ref:
        rar_ref.extractall(to)

    # go through all files
    onlyfiles = [f for f in listdir(to) if isfile(join(to, f))]
    for f in onlyfiles:
        try:
            unrar(to + '/' + f, without_extension(to + '/' + f))
            remove_file(from_dir)
        except Exception:
            print(f + ' is not a zip folder')

    # go through all folders
    onlyfolders = [f for f in listdir(to) if not isfile(join(to, f))]
    for f in onlyfolders:
        unrar_folder(to + '/' + f)

def unrar_folder(path):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        for f in onlyfiles:
            try:
                unrar(path + '/' + f, without_extension(path + '/' + f))
                remove_file(path + '/' + f)

            except Exception:
                print(f + ' is not a zip folder')

        # go through all folders
        onlyfolders = [f for f in listdir(path) if not isfile(join(path, f))]
        for f in onlyfolders:
            unrar_folder(path + '/' + f)  


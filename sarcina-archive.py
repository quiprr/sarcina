#!/usr/bin/env python3
"""
sarcina-archive,

a python script as an alternative to dpkg-scanpackages or apt-ftparchive
"""

# Imports
import zstandard as zstd
import unix_ar as ar
import lzma as xz
import hashlib
import tarfile
import gzip
import time
import yaml
import bz2
import sys
import os

# Static Declarations; edit these as you need to conform to your system
PACKAGES_DIR = "./iphoneos-arm"
REPO_DIR = "./"
REPO_CONFIG = "./meta/repo.yml"

ICON_URL = "https://repo.quiprr.dev/assets"
WEBDEPICTION_URL = "https://repo.quiprr.dev/depictions/web/?p="
SILEODEPICTION_URL = "https://repo.quiprr.dev/depictions/native"

finalControlData = bytes("", "utf-8")

startTime = time.time()
revisions = 0

def getSize(file):
    return os.path.getsize(file)

def getMd5(file):
    return hashlib.md5(open(file, 'rb').read()).hexdigest()

def getSha1(file):
    return hashlib.sha1(open(file, 'rb').read()).hexdigest()

def getSha256(file):
    return hashlib.sha256(open(file, 'rb').read()).hexdigest()

def getSha512(file):
    return hashlib.sha512(open(file, 'rb').read()).hexdigest()

if not PACKAGES_DIR or not REPO_DIR:
    print("One of your directory statics are empty. Please fill said static with the correct path, then run this script.")
    exit()

for filename in os.listdir(f'{PACKAGES_DIR}'):
    if filename.endswith(".deb"):
        finalControlData += tarfile.open(fileobj=ar.open(f'{PACKAGES_DIR}/' + filename).open('control.tar.xz')).extractfile('./control').read()
        finalControlData += bytes("\n", "utf-8")
        revisions += 1

with open("Packages", "w+") as packagesFile:
    packagesFile.write(finalControlData.decode('utf-8'))

with open("Packages.xz", "wb+") as packagesXzFile:
    packagesXzFile.write(xz.compress(finalControlData))

with open("Packages.bz2", "wb+") as packagesBz2File:
    packagesBz2File.write(bz2.compress(finalControlData))

with open("Packages.gz", "wb+") as packagesGzFile:
    packagesGzFile.write(gzip.compress(finalControlData))

with open("Packages.zst", "wb+") as packagesZstFile:
    packagesZstFile.write(zstd.ZstdCompressor().compress(finalControlData))

with open("Release.temp", "w+") as tempReleaseFile:
    configData = open(REPO_CONFIG, "r").read()
    tempReleaseFile.write(configData)

with open("Release", "w+") as releaseFile:
    releaseFile.write(configData)
    releaseFile.write(f"\nMD5Sum:\n {hashlib.md5(open('Packages', 'r').read().encode('utf-8')).hexdigest()}            {getSize('Packages')} Packages")
    releaseFile.write(f"\n {getMd5('Packages.bz2')}             {getSize('Packages.bz2')} Packages.bz2")
    releaseFile.write(f"\n {getMd5('Packages.gz')}             {getSize('Packages.gz')} Packages.gz")
    releaseFile.write(f"\n {getMd5('Packages.xz')}             {getSize('Packages.xz')} Packages.xz")
    releaseFile.write(f"\n {getMd5('Packages.zst')}             {getSize('Packages.zst')} Packages.zst")
    releaseFile.write(f"\n {hashlib.md5(open('Release.temp', 'r').read().encode('utf-8')).hexdigest()}              {getSize('Release.temp')} Release")

    releaseFile.write(f"\nSHA1:\n {hashlib.sha1(open('Packages' ,'r').read().encode('utf-8')).hexdigest()}            {getSize('Packages')} Packages")
    releaseFile.write(f"\n {getSha1('Packages.bz2')}             {getSize('Packages.bz2')} Packages.bz2")
    releaseFile.write(f"\n {getSha1('Packages.gz')}             {getSize('Packages.gz')} Packages.gz")
    releaseFile.write(f"\n {getSha1('Packages.xz')}             {getSize('Packages.xz')} Packages.xz")
    releaseFile.write(f"\n {getSha1('Packages.zst')}             {getSize('Packages.zst')} Packages.zst")
    releaseFile.write(f"\n {hashlib.sha1(open('Release.temp', 'r').read().encode('utf-8')).hexdigest()}              {getSize('Release.temp')} Release")

    releaseFile.write(f"\nSHA256:\n {hashlib.sha256(open('Packages' ,'r').read().encode('utf-8')).hexdigest()}            {getSize('Packages')} Packages")
    releaseFile.write(f"\n {getSha256('Packages.bz2')}             {getSize('Packages.bz2')} Packages.bz2")
    releaseFile.write(f"\n {getSha256('Packages.gz')}             {getSize('Packages.gz')} Packages.gz")
    releaseFile.write(f"\n {getSha256('Packages.xz')}             {getSize('Packages.xz')} Packages.xz")
    releaseFile.write(f"\n {getSha256('Packages.zst')}             {getSize('Packages.zst')} Packages.zst")
    releaseFile.write(f"\n {hashlib.sha256(open('Release.temp', 'r').read().encode('utf-8')).hexdigest()}              {getSize('Release.temp')} Release")

    releaseFile.write(f"\nSHA512:\n {hashlib.sha512(open('Packages' ,'r').read().encode('utf-8')).hexdigest()}            {getSize('Packages')} Packages")
    releaseFile.write(f"\n {getSha512('Packages.bz2')}             {getSize('Packages.bz2')} Packages.bz2")
    releaseFile.write(f"\n {getSha512('Packages.gz')}             {getSize('Packages.gz')} Packages.gz")
    releaseFile.write(f"\n {getSha512('Packages.xz')}             {getSize('Packages.xz')} Packages.xz")
    releaseFile.write(f"\n {getSha512('Packages.zst')}             {getSize('Packages.zst')} Packages.zst")
    releaseFile.write(f"\n {hashlib.sha512(open('Release.temp', 'r').read().encode('utf-8')).hexdigest()}              {getSize('Release.temp')} Release")

os.remove('Release.temp')

elapsed = time.time() - startTime
print(f"Sarcina has completed {revisions} packages in {round(elapsed, 4)} seconds.")
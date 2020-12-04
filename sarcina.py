#!/usr/bin/env python3
"""
sarcina,

a python script to forcefully add depictions to
a debian package's `control` file, automatically.
"""

# Imports
import logging
import shutil
import time
import yaml
import sys
import os

# Static Declarations; edit these as you need to conform to your system
PACKAGES_DIR = "./iphoneos-arm"
TEMP_DIR = "./__temp__"
REPO_DIR = "./"

APTFTPARCHIVE = "apt-ftparchive"
GZIP = "gzip"
BZIP2 = "bzip2"
XZIP = "xz"
ZSTANDARD = "zstd"

ICON_URL = "https://repo.quiprr.dev/assets"
WEBDEPICTION_URL = "https://repo.quiprr.dev/depictions/web/?p="
SILEODEPICTION_URL = "https://repo.quiprr.dev/depictions/native"

# Logging Setup
root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
startTime = time.time()
revisions = 0

def removePackages():
    try:
        os.remove(f"{REPO_DIR}/Packages")
    except:
        pass
    try:
        os.remove(f"{REPO_DIR}/Packages.gz")
    except:
        pass
    try:
        os.remove(f"{REPO_DIR}/Packages.bz2")
    except:
        pass
    try:
        os.remove(f"{REPO_DIR}/Packages.xz")
    except:
        pass
    try:
        os.remove(f"{REPO_DIR}/Packages.zst")
    except:
        pass

def removeTempFiles():
    try:
        shutil.rmtree(TEMP_DIR)
    except:
        pass
    try:
        os.mkdir(TEMP_DIR)
    except:
        pass

def generatePackages():
    os.system(f"{APTFTPARCHIVE} -q -q packages {PACKAGES_DIR} > Packages")
    os.system(f"{GZIP} -c9 Packages > Packages.gz")
    os.system(f"{BZIP2} -c9 Packages > Packages.bz2")
    os.system(f"{XZIP} -c9 Packages > Packages.xz")
    os.system(f"{ZSTANDARD} -q -c19 Packages > Packages.zst")

def generateRelease():
    os.system(f"{APTFTPARCHIVE} -q -q release -c meta/repo.conf . > Release")

if not PACKAGES_DIR or not TEMP_DIR or not REPO_DIR:
    logging.fatal("One of your directory statics are empty. Please fill said static with the correct path, then run this script.")
    exit()

if not APTFTPARCHIVE or not GZIP or not BZIP2 or not XZIP or not ZSTANDARD:
    logging.fatal("One of your executable statics are empty. Please fill said static with the correct path, then run this script.")
    exit()

logging.debug("All necessary statics exist.")

for root, dirs, files in os.walk(PACKAGES_DIR):
    for packageName in files:
        if packageName.endswith('.deb'):
            packageTempDirName = packageName[:-len(".deb")]
            os.mkdir(f"{TEMP_DIR}/{packageTempDirName}")
            os.system(f"dpkg-deb --raw-extract {PACKAGES_DIR}/{packageName} {TEMP_DIR}/{packageTempDirName} 1>/dev/null")
            logging.debug(f"Package {PACKAGES_DIR}/{packageName} extracted to directory {TEMP_DIR}/{packageTempDirName}.")
            with open(f'{TEMP_DIR}/{packageTempDirName}/DEBIAN/control', 'r') as controlFile:
                controlData = yaml.load(controlFile, Loader=yaml.FullLoader)
                packageBundleIdentifier = controlData["Package"]
                controlData["Icon"] = f"{ICON_URL}/{packageBundleIdentifier}.png"
                controlData["Depiction"] = f"{WEBDEPICTION_URL}{packageBundleIdentifier}"
                controlData["SileoDepiction"] = f"{SILEODEPICTION_URL}/{packageBundleIdentifier}/depiction.json"
            with open(f'{TEMP_DIR}/{packageTempDirName}/DEBIAN/control', 'w') as controlFile:
                pkgStartTime = time.time()
                yaml.dump(controlData, controlFile)
                os.remove(f"{PACKAGES_DIR}/{packageName}")
                os.system(f"dpkg-deb -b {TEMP_DIR}/{packageTempDirName} {PACKAGES_DIR}/{packageName} 1>/dev/null")
                elapsed = time.time() - pkgStartTime
                logging.info(f"Completed package {packageName} in {round(elapsed, 2)} seconds.")
                revisions += 1

removeTempFiles()
removePackages()
generatePackages()
generateRelease()

elapsed = time.time() - startTime
logging.info(f"Sarcina has completed packaging {revisions} packages and Release in {round(elapsed, 2)} seconds.")
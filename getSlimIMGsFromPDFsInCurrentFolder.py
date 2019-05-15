#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
from itertools import chain
from pathlib import WindowsPath

LIMIT_SIZE_OF_IMG = 1024 * 1024 * 0.7


def extractIMGs(pdf):
    print(pdf)
    pdf = WindowsPath(pdf)
    folder = pdf.parent
    name = pdf.stem

    oldset = set(
        chain(folder.glob('*.jpg'), folder.glob('*.jpeg'),
              folder.glob('*.png')))
    os.system(f"mutool extract {pdf}")
    newset = set(
        chain(folder.glob('*.jpg'), folder.glob('*.jpeg'),
              folder.glob('*.png')))
    imgset = newset - oldset
    imgnum = len(imgset)

    digit_width = len(str(len(imgset)))

    result = []
    for i, img in enumerate(imgset):
        extname = WindowsPath(img).suffix
        if imgnum > 1:
            imgname = f"{name}_{i:0{digit_width}{extname}}"
        else:
            imgname = f"{name}{extname}"
        newimg = pdf.with_name(imgname)
        shutil.move(img, newimg)
        result.append(newimg)
    return result


def silmIMG(img):
    imgsize = os.path.getsize(img)
    quality = LIMIT_SIZE_OF_IMG / imgsize * 100
    os.system(
        f"magick -compress JPEG -quality {quality} {img} -colors 8 new_{img}")
    shutil.move(f"new_{img}", f"{img}")


def getSlimIMGsFromPDFsInFolder(folder):
    folder = WindowsPath(folder)
    for pdf in folder.glob('*.pdf'):
        imglst = extractIMGs(pdf)
        for img in imglst:
            silmIMG(img)


if __name__ == "__main__":
    workdir = WindowsPath('.')
    getSlimIMGsFromPDFsInFolder(workdir)

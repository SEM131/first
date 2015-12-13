import os
from ftplib import FTP
from zipfile import ZipFile
import xml.etree.ElementTree as etree

def download(ftp, file):
    ftp.retrbinary('RETR ' + file, open(file, 'wb').write)

def parse(ftp):
    data = ftp.nlst()
    list = []
    for file in data:
        print(file)
        download(ftp,file)
        readxml(file,list)
        os.remove(file)
    for i in list: print(i)
    list.clear()

def readxml(file,list):
    zip = ZipFile(file, 'r')
    tree = etree.parse(zip.open(zip.namelist()[0]))
    for i in tree.getroot()[0]:
        try:
            if i[21][0].text == '1322500' and not i[13].text in list: list.append(i[13].text)
        except IndexError: continue
    zip.close()

ftp=FTP('ftp.zakupki.gov.ru')
ftp.login('free', 'free')
ftp.cwd('fcs_nsi/nsiOrganization')
parse(ftp)

ftp.quit()

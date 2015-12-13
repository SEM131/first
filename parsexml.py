import os
from ftplib import FTP
from zipfile import ZipFile
import xml.etree.ElementTree as etree

def download(ftp, file):
    ftp.retrbinary('RETR ' + file, open(file, 'wb').write)

def parse(ftp):
    data = ftp.nlst()
    for file in data:
        #print(file)
        download(ftp,file)
        readxml(file)
        os.remove(file)

def readxml(file):
    zip = ZipFile(file, 'r')
    tree = etree.parse(zip.open(zip.namelist()[0]))
    for i in tree.getroot()[0]:
        try:
            if i[21][0].text == '1322500': print(i[13].text, i[1].text)
        except IndexError: continue
    zip.close()

ftp=FTP('ftp.zakupki.gov.ru')
ftp.login('free', 'free')
ftp.cwd('fcs_nsi/nsiOrganization')
parse(ftp)

ftp.quit()

import os
from ftplib import FTP
from zipfile import ZipFile
import xml.etree.ElementTree as etree

def download(ftp, file):
    ftp.retrbinary('RETR ' + file, open(file, 'wb').write)

def parseorg(ftp,list):
    ftp.cwd('/fcs_nsi/nsiOrganization')
    data = ftp.nlst()
    for file in data: readxmlorg(file,list)

def readxmlorg(file,list):
    print(file)
    download(ftp,file)
    zip = ZipFile(file, 'r')
    tree = etree.parse(zip.open(zip.namelist()[0]))
    for i in tree.getroot()[0]:
        try:
            if i[21][0].text == '1322500' and not i[13].text in list: list.append(i[13].text)
        except IndexError: continue
    zip.close()
    os.remove(file)

def parsereg(ftp,list):
    ftp.cwd('/fcs_regions')
    for line in ftp.nlst():
        if line == '_logs': break
        ftp.cwd('/fcs_regions/'+line+'/notifications')
        for file in ftp.nlst():
            readxmlreg(file,list,line)
        ftp.cwd('currMonth')
        for file in ftp.nlst():
            readxmlreg(file,list,line)

def readxmlreg(file,list,line):
    if file[-4:] != '.zip': return
    print(file)
    download(ftp,file)
    zip = ZipFile(file, 'r')
    for xml in zip.namelist():
        tree = etree.parse(zip.open(xml))
        for i in tree.getroot():
            try:
                if i[6][0][4].text in list: zip.extract(xml, 'regions/'+line+'/'+i[6][0][4].text)
            except IndexError: continue
    zip.close()
    os.remove(file)

ftp=FTP('ftp.zakupki.gov.ru')
ftp.login('free', 'free')
inn = []
parseorg(ftp,inn)
parsereg(ftp,inn)

ftp.quit()

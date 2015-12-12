import os
from ftplib import FTP
from zipfile import ZipFile
import xml.etree.ElementTree as etree

def download(ftp, file):
    ftp.retrbinary('RETR ' + file, open(file, 'wb').write)

def parse(ftp):
    data = ftp.nlst()
    for file in data:
        print(file)
        download(ftp,file)
        readxml(file)
        os.remove(file)
        

def readxml(file):
    zip = ZipFile(file, 'r')
    xmlfile = zip.open(zip.namelist()[0])
    tree = etree.parse(xmlfile)
    root = tree.getroot()
    i =0
    while i<3000:
        try :
            if root[0][i][21][0].text == '1322500':
            #if root[0][i][21][1].text== 'Министерство образования и науки Российской Федерации':
                #print(root[0][i][21][1].text)
                print (root[0][i][1].text)
                print (root[0][i][13].text)
        except IndexError:
            i+=1
            continue
        i=i+1
    zip.close()

ftp=FTP('ftp.zakupki.gov.ru')
ftp.login('free', 'free')
ftp.cwd('fcs_nsi/nsiOrganization')
parse(ftp)


ftp.quit()

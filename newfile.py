from ftplib import FTP
import sys

def searchnew(ftp):
    folder=''
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    while folder[-7:] != 'xml.zip':
        if folder != '': ftp.cwd(folder)
        data=[]
        new=[0,'','','','']
        ftp.dir(data.append)
        for line in data:
            if line[52] == ':':
                if line[-4] == '.' and line[-7:] != 'xml.zip': continue
                mon = months.index(line[43:46])
                day = line[47:49]
                hour = line[50:52]
                minute = line[53:55]
                if new[0] < mon or new[0] == mon and new[1] < day or new[0] == mon and new[1] == day and new[2] <= hour and new[3] < minute:
                    new=[mon,day,hour,minute,line[56:]]
        folder=new[4]
    else: return folder
    
def download(ftp, file):     
    ftp.retrbinary('RETR ' + file, open(file, 'wb').write)

ftp=FTP('ftp.zakupki.gov.ru')
ftp.login('free', 'free')

newfile=searchnew(ftp)
print(newfile)
download(ftp, newfile)

ftp.quit()
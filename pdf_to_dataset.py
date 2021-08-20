import os
import textract
from os.path import isfile, join


foldername="legalpdf/"
txtpath="txtfiles/"


def createdir(path):
  try:
    os.mkdir(path)
  except OSError as er:
    print(er)


def pdf_to_txt(x):
  try:
    filepath=foldername+x
    text = textract.process(filepath).decode("utf-8")
    dstfile=txtpath+x[0:-4]+".txt"
    print("File %s Converted to %s"%(filepath, dstfile))
    file=open(dstfile,"w")
    file.writelines(text)
    file.close()
  except OSError as er:
    print(er)


onlyfiles = [f for f in os.listdir(foldername) if isfile(join(foldername, f))]
print(len(onlyfiles))

createdir(txtpath)

#for i in range(len(onlyfiles)):
#  try:
#    pdf_to_txt(onlyfiles[i])
#  except OSError as er:
#    print(er,i)

print(onlyfiles[0])
#.decode("utf-8")
print(textract.process(foldername+onlyfiles[0]))


#for i in onlyfiles:
#  pdf_to_txt(i)




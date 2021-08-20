import os
from os.path import isfile, join

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser


import csv


def convert_pdf_to_string(file_path):
  output_string = StringIO()
  with open(file_path, 'rb') as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
      interpreter.process_page(page)

  return (output_string.getvalue())




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
    text=convert_pdf_to_string(filepath)
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

filepath='legalpdf/2011LHC4000.pdf'


text = convert_pdf_to_string(filepath)
print(text)



#for i in onlyfiles:
#  pdf_to_txt(i)



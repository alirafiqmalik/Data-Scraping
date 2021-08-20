from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from multiprocessing import Process
from os.path import isfile, join
from io import StringIO

import time
import os




foldername="legalpdf/"
txtpath="txtfiles/"


def createdir(path):
  try:
    os.mkdir(path)
  except OSError as er:
    print(er)



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




def pdf_to_txt(x):
  try:
    filepath=foldername+x
    text=convert_pdf_to_string(filepath)
    dstfile=txtpath+x[0:-4]+".txt"
    file=open(dstfile,"w")
    file.writelines(text)
    file.close()
    print("File %s Converted to %s" % (filepath, dstfile))
  except:
    print("########################   ERROR   ########################")


IncompleteError=[]
def multiprocess(f,tasks,timeout = 120,pool_len = 60):
  procs = []
  while len(tasks) > 0 or len(procs) > 0:
    if len(tasks) > 0 and len(procs) < pool_len:
      n = tasks.pop(0)
      p = Process(target=f, args=(n,))
      p.start()
      procs.append({'n': n, 'p': p, 't': time.time() + timeout})
    for d in procs:
      if not d['p'].is_alive():
        procs.remove(d)
        #print ('%s'% d['n'])
      elif d['t'] < time.time():
        d['p'].terminate()
        procs.remove(d)
        IncompleteError.append(d['n'])
        print( 'Timeout Process Killed for = %s ' % d['n'])
    time.sleep(0.05)



if __name__ == "__main__":
  onlyfiles = [f for f in os.listdir(foldername) if isfile(join(foldername, f))]
  print(len(onlyfiles))

  createdir(txtpath)

  #filepath = 'legalpdf/2011LHC4000.pdf'

  multiprocess(pdf_to_txt,onlyfiles,pool_len = 60)



import os
import urllib.request
from multiprocessing import Process
import time



foldername="legalpdf/"
IncompleteError=[]


def removefiles(folderpath,files):
  for i in files:
    try:
      os.remove(folderpath+i)
    except:
      print("File not found",folderpath+i)


def createdir(path):
  try:
    os.mkdir(path)
  except OSError as er:
    print(er)


def remainingfiles(x,folderpath):
    dfiles=[i for i in os.listdir(folderpath)]
    return [value for value in x if value.split("/")[-1] not in dfiles]


def downloadpdf(x):
    try:
        urllib.request.urlretrieve(x,foldername+x.split("/")[-1])
        print("Download Finished for =", x)
    except:
        print("Link Error for =",x)



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
    file = open("links.txt")
    x = file.read().split("\n")
    print(len(x))

    createdir(foldername)
    cond=True
    count=0
    timeout = 120
    while cond:
        count+=1
        print("Before",len(x),x)
        x = remainingfiles(x, foldername)
        print("After",len(x),x)
        IncompleteError = []
        multiprocess(downloadpdf, x,timeout = timeout)
        errorcount = len(IncompleteError)
        print(errorcount)
        if errorcount == 0:
            cond = False
        else:
            timeout = 2*timeout
            removefiles(foldername, IncompleteError)
        print("Loop done", count)
        print("No of Files Downloaded=", len(x)-errorcount)
        print("No of Files Not Downloaded=", errorcount)
        if count>2:
            print("To Many Retries, Ending Loop")
            break

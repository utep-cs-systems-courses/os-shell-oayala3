#! /usr/bin/env python3

import os, sys, time, re, array

pid = os.getpid()

ps1="$"

buff= ""
lBuff= ""
nextChar = 0
limit = 0
lLimit = 0
nextLine = 0

def getChar():
    
    global nextChar
    global limit
    global buff
    if(nextChar==limit):
        nextChar = 0
        buffByte = os.read(0,1000)
        print("after read")
        buff=str(buffByte, 'utf-8')
        limit=len(buff)
        if(limit==0):
            return 0
    c=buff[nextChar]
    if(c=="\n"):
        limit=0
        buff=""
        nextChar=0
        return -1
    else:
        nextChar+=1
        return c

def getLine():
    line=""
    c=getChar()
    
    while(c!=0 and c != -1 ):
        line += c
        c=getChar()
    if(len(line)>0):
        return line
    else:
        return "0"

def interpreter(line):
    args=line.split()
    if(args[0]=="exit"):
        return -1
    elif(args[0]=="PS1"):
        ps1Update(args[2])
        print(args[0])
    else:
        callExec(args)
        


def callExec(args)
pid = os.getpid()

os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
rc = os.fork()
if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
elif rc == 0:                   # child
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n"(os.getpid(), pid)).encode())
        args = ["wc", "p3-exec.py"]

        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())

            try:
                os.execve(program, args, os.environ) # try to exec program

            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly
        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())

        sys.exit(1)                 # terminate with error

else:                           # parent (forked ok)
    os.write(1, ("Parent: My pid=%d.  Child's  pid=%d\n" % (pid, rc)).encode())
    childPidCode = os.wait()
    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())

def ps1Update(promt):
    
    global ps1
    ps1=promt+" "

    
                     
numLines = -1

while True:
    numLines+=1
    os.write(1,ps1.encode())
    line=getLine()
    if(line == "0"):
        break
    else:
        interpreter(line)
           
print("end")

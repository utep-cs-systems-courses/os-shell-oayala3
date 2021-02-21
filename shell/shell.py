#! /usr/bin/env python3

import os, sys, time, re, array


ps1="$"
buff= ""
lBuff= ""
nextChar = 0
limit = 0
lLimit = 0
nextLine = 0
reDirI=False
reDirO=False
inFile=""
outFile=""
agrs1=[]
args2=[]


def getChar():
    
    global nextChar
    global limit
    global buff
    if(nextChar==limit):
        nextChar = 0
        buffByte = os.read(0,1000)
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
    command=line.split()
    if(command[0]=="exit"):
        return False
    elif(command[0]=="PS1"):
        ps1Update(command[2])
        return True
    elif(command[0]=="CD"):
        cd(command)
        return True
    elif(command[0]=="PWD"):
        cd()
        return True
    elif(checkPipe()):
        pipeExec()
    else:
        checkReDirect(command)
        callExec(command)
        return True

def cd(path):
    os.chdir(path)
def pwd():
    location=os.getcwd()
    os.write(1, (location).encode())
    
def checkPipe(command):
    global pipe
    global args1
    global args2
    while(i<len(command) and !pipe):
        if(command[i]=="|"):
            pipe = True
            args1 = getArgs(0,i-1,command)
            args2 = getArgs(i+1,len(command)-1,command)
        else:
            i+=1
def getArgs(first,last,command):
agrs = []
while(first<last):
    args=args+command[first]
    first+=1
return args
        
def checkReDirect(command):
    global inFile
    global outFile
    global reDirI
    global reDirO

    reDirI=False
    reDirO=False
    
    for i in command:
        if(i==">"):
            reDirO=True
            outFile=i+1
        elif(i=="<"):
            reDirI=True;
            inFile=i+1
          

def reDirectInput():
    global inFile
    os.close(0)                 # redirect child's stdout
    os.open(inFile, os.O_RDONLY);
    os.set_inheritable(0, True)
    args=getLine().split()
    return args
    
def reDirectOutput():
    global outFile
    os.close(1)                 # redirect child's stdout
    os.open(outFile, os.O_CREAT | os.O_WRONLY);
    os.set_inheritable(1, True)
    
def callExec(args):
    
    pid = os.getpid()
    
    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:                   # child
        
        if(reDirI):
            args=reDirectInput()
        if(reDirO):
            reDirectOutput()

        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())

        execFuntion(args);

    else:                           # parent (forked ok)
        os.write(1, ("Parent: My pid=%d.  Child's  pid=%d\n" % (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())

def execFuntion(args):
    for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())

            try:
                os.execve(program, args, os.environ) # try to exec program

            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly
        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())

        return sys.exit(1)                 # terminate with error

        
def pipeExec(args1, args2):
    pid = os.getpid()               # get and remember pid
    pr,pw = os.pipe()
    for f in (pr, pw):
            os.set_inheritable(f, True)
            print("pipe fds: pr=%d, pw=%d" % (pr, pw))
            import fileinput
            print("About to fork (pid=%d)" % pid)
            rc = os.fork()
            if rc < 0:
                    print("fork failed, returning %d\n" % rc, file=sys.stderr)             
                    sys.exit(1)
            elif rc == 0:                   #  child - will write to pipe
                print("Child: My pid==%d.  Parent's pid=%d" % (os.getpid(), pid), file=sys.stderr)                
                   
                os.close(1)                 # redirect child's stdout  
                os.dup(pw)
                for fd in (pr, pw):
                    os.close(fd)                        
                execFuntion(args1)

            else:                           # parent (forked ok)
                print("Parent: My pid==%d.  Child's pid=%d" % (os.getpid(), rc), file=sys.stderr)
                os.close(0)
                os.dup(pr)
                for fd in (pw, pr):
                    os.close(fd)
                execFuntion(args2)
        
def ps1Update(promt):   
    global ps1
    ps1=promt+" "

    
                     
numLines = -1
cont=True

while cont:
    numLines+=1
    os.write(1,ps1.encode())
    line=getLine()
    if(line == "0"):
        cont=False
    else:
        cont = interpreter(line)
           
print("end")

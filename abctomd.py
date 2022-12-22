import eecpid

from tkinter import *
from tkinter import ttk



def get_v():
    ent.get()
    ent2.get()
    root.destroy()
    return ent

root = Tk()
root.geometry("250x200")
root.title("Enter file names")
ent = StringVar()
ent2 = StringVar()

label = Label(root, text='Enter .pas file name')
label.pack(anchor=NW, padx=8, pady=2)

entry = ttk.Entry(root, textvariable=ent)
entry.pack(anchor=NW, padx=8, pady=4)

label = Label(root, text='Enter .md file name')
label.pack(anchor=NW, padx=8, pady=2)

entry2 = ttk.Entry(root, textvariable=ent2)
entry2.pack(anchor=NW, padx=8, pady=4)



btn = ttk.Button(root, text="Enter", command=get_v)
btn.pack(anchor=NW, padx=6, pady=6)

root.mainloop()
entv = ''
entv2 = ''
entv = ent.get()
entv2 = ent2.get()



startread = False
beginread = 0
endread = 0
filestop = False
analysis = []
dl = []
ll = []

#file = open("pabcfile2.pas")
file = open(entv + ".pas")
n = file.read()
file.close()
n = n[3:]

def nextabc(s):
    f = 0
    for i in range(s,len(n)):
        if n[i] == ';' or n[i] == '\n' or i == len(n)-1 or n[i:i+2] == '. ' or n[i:i+2] == '.\n':
            f = i
            break
        if n[i:i+3] == 'do ' or n[i:i+3] == 'do\n':
            f = i + 3
            break
        if n[i:i+4] == 'end ' or n[i:i+4] == 'end\n':
            f = i + 4
            break
        if n[i:i + 5] == 'then ' or n[i:i + 5] == 'then\n':
            f = i + 5
            break
        if n[i:i + 5] == '\nelse' or n[i:i + 5] == ' else':
            f = i
            break
        if n[i:i + 6] == 'begin\n' or n[i:i + 6] == 'begin ':
            f = i + 6
            break
    return f

def extractabc(s,f):
    r = ''
    r += n[s:f]
    return r


def to_str_id(n: int) -> str:
    res = ''
    if 0 < n < 27:
        res = chr(n - 1 + ord('A'))
    elif 26 < n < 53:
        res = chr(n - 27 + ord('a'))
    else:
        first = n // 52
        if n % 52 == 0: first -= 1
        second = n % 52
        if second == 0: second = 52

        if 0 < first < 27:
            res += chr(first - 1 + ord('A'))
        elif 26 < first < 53:
            res += chr(first - 27 + ord('a'))

        if 0 < second < 27:
            res += chr(second - 1 + ord('A'))
        elif 26 < second < 53:
            res += chr(second - 27 + ord('a'))
    return res



for i in range(len(n)):
    if n[i:(i+5)] == 'begin':
        beginread = i+6
        break
while filestop == False:
    endread = nextabc(beginread)
    analysis.append(extractabc(beginread,endread))
    beginread = endread + 1
    if n[endread:endread+2] == '. ' or n[endread:endread+2] == '.\n' or endread == len(n)-1:
        filestop = True



eecpid.formatd(analysis)
analysis = eecpid.nospace(analysis)
depth = 0
for n in analysis:
    if 'begin' in n:
        depth += 1
    if 'end' in n:
        depth -= 1
    ll.append(depth)
dl = analysis.copy()


chg = 66





for n in range(len(dl)):
    dl[n] = dl[n].replace('(',' ')
for n in range(len(dl)):
    dl[n] = dl[n].replace(')',' ')






assigns = eecpid.iden(dl,ll)


qtr = 0
qf = False
elseresolve = False
elseresmem = 0
#filemd = open("obsfile.md", 'w')
filemd = open(entv2 + ".md", 'w')
filemd.write('```mermaid\ngraph TB\n')

filemd.write('A(begin)\n')
for n in range(len(dl)):
    filemd.write(to_str_id(n + 2))
    if assigns[n] == 'q':
        filemd.write('{' + dl[n] + '}\n')
        filemd.write(to_str_id(n + 1) + ' -->' + to_str_id(n + 2) + '\n')
    elif assigns[n] == 'else':
        filemd.write('[' + dl[n] + ']\n')
        qf = False
        qtr = n
        while not qf:
            if assigns[qtr] == 'q' and ll[qtr] == ll[n]:
                qf = True
            else:
                qtr -= 1
        filemd.write(to_str_id(qtr+2) + ' -->' + to_str_id(n + 2) + '\n')
        if ll[n] < ll[n+1]:
            elseresolve = True
            elseresmem = n
        else:
            filemd.write(to_str_id(n + 1) + ' -->' + to_str_id(n + 4) + '\n')


    else:
        if dl[n] == 'end':
            filemd.write('(' + dl[n] + ')\n')
        elif 'while ' == dl[n][:6] or dl[n][:7] == 'repeat ' or dl[n][:4] == 'for ':
            filemd.write('>' + dl[n] + ']\n')
        else:
            filemd.write('[' + dl[n] + ']\n')

        filemd.write(to_str_id(n + 1) + ' -->' + to_str_id(n + 2) + '\n')


    ## RESOLVING

    if elseresolve:
        if ll[n+1] < ll[n]:
            filemd.write(to_str_id(elseresmem + 1) + ' -->' + to_str_id(n + 4) + '\n')
            elseresolve = False





filemd.write('```\n')
filemd.close()



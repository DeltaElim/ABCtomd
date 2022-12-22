def formatd(dl):
    for a in range(0,len(dl)):
        dl[a] = dl[a].replace('\n', '')
    for a in range(0, len(dl)):
        r = False
        if dl[a] != '':
            while not r:
                if dl[a]!='':
                    if dl[a][0] == ' ':
                        dl[a] = dl[a][1:]
                    else:
                        r = True
                else:
                    r = True
    for a in range(0, len(dl)):
        r = False
        if dl[a] != '':
            while not r:
                if dl[a] != '':
                    if dl[a][len(dl[a])-1:] == ' ':
                        dl[a] = dl[a][:len(dl[a])-1]
                    else:
                        r = True
                else:
                    r = True



def idenout(dl,ll):
    a = 0
    for n in dl:
        if n == 'begin':
            print('     ' *ll[a-1] + n)
            a += 1
        else:
            print('     '*ll[a] + n)
            a += 1


def iden(dl,ll):
    isq = False
    oisq = False
    ise = False
    oise = False
    output = []
    for n in range(len(dl)):

        if dl[n][:3] == 'if ':
            output.append('q')
            isq = True
            if ll[n] == ll[n+1]:
                oisq = True
        elif dl[n] == 'else':
            output.append('else')
            ise = True
            if ll[n] == ll[n+1]:
                oise = True

        else:
            output.append('zero')
    return output

def nospace(dl):
    done = False
    while not done:
        done = True
        for n in range(0,len(dl)):
            if dl[n] == '':
                done = False
                dl.pop(n)
                break

    return dl


# if isq:
#     if oisq:
#         output.append('qy')
#         oisq = False
#         isq = False
#     else:
#         output.append('qy')
#         if ll[n] > ll[n + 1]:
#             isq = False
# elif ise:
#     if oise:
#         output.append('qn')
#         oise = False
#         ise = False
#     else:
#         output.append('qn')
#         if ll[n] > ll[n + 1]:
#             ise = False







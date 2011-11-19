def extractAgrs(paramsList):
    return dict(map(lambda x:(x[:x.index('=')], x[x.index('=')+1:]), paramsList))

def ask(message, validOptions={'y':True,'n':False}, input=raw_input):
    yesno =''
    if isinstance(validOptions, str):
        #print validOptions
        yesno = input(message)
    else:
        #print validOptions.keys()
        yesno = input(message+'('+'/'.join(validOptions.keys())+'):')
    while True:
        if validOptions=='*':
            return yesno
        if len(yesno)>0: 
            if validOptions.has_key(yesno):
                return validOptions[yesno]
        print 'Not Valid Input'
        yesno = input(message+'('+'/'.join(validOptions.keys())+'):')

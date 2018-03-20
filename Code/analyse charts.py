import os
def Analysing_charts():
    for filename in os.listdir("C:/Users/Antony/Documents/GitHub/exeter_pubs/Text files")[:len(os.listdir("C:/Users/Antony/Documents/GitHub/exeter_pubs/Text files"))-1]:
        with open("C:/Users/Antony/Documents/GitHub/exeter_pubs/Text files/" + filename, 'r') as myfile:
            data = myfile.read().replace('\n', '')
            myfile.close()
##        charts = [(i, data[i:i+16]) for i in findall('Chart', data)]
##        dic = {}
##        for chart in charts:
##            x = chart[1]
##            y = chart[0]
##            if data[y+6] == 's':
##                if data[y+8:y+10].isdigit():
##                    pass
##                else:
##                    charts.remove(chart)
##            if data[y+8:y+9].isdigit():
##                pass
##            else:
##                charts.remove(chart)
##            if data[y+5] == 'e':
##                try:                        # Try and remove it
##                    charts.remove(chart)
##                except ValueError:          # If it cant find it in the list 
##                    pass                    # Do nothing (continue on)
##            count = data.count(x)
##            if count > 0:
##                dic[x] = count
##
##        print(dic)
##                
##def findall(p, s):
##    i = s.find(p)
##    while i != -1:
##        yield i
##        i = s.find(p, i+1)


        charts = [(i, data[i:i+3]) for k in [ list(findall(j, data)) for j in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]] for i in k]
        dic = {}
        for chart in charts:
            x = chart[1]
            y = chart[0]
            if x.isdigit():
                pass
            else:
                charts.remove(chart)
            if data[y-20:y-1].lower().count('chart') > 0:
                pass
            else:
                try:
                    charts.remove(chart)
                except:
                    pass
            count = data.count(x)
            if count > 0:
                dic[x] = count

        print(dic)
                
def findall(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)


Analysing_charts()

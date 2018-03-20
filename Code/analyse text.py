import os, csv, pickle


def Comparing_txt():
    name = os.getcwd()
    master_dic = {}
    for filename in os.listdir(os.path.join(name, "Text files"))[:len(os.listdir(os.path.join(name, "Text files")))-1]:
        with open(os.path.join(name, "Text files/{0}".format(filename)), mode='r',errors='ignore') as myfile:
            data = myfile.read().replace('\n', '')
            myfile.close()
            with open(os.path.join(name, "Requisites/Publication_Names.csv"), mode='r', errors='ignore') as csvfile:
                places = csv.DictReader(csvfile)
                places_dict = {}
                for row in places:
                    places_dict[row["NP"]] = row["Title"]
##                print(places_dict)
            dic = {}
        for key,title in places_dict.items():
            count = data.count(title)
            if count > 0:
                dic[key] = count
        master_dic[filename[filename.find("NP"):filename.find("NP")+4]] = dic
    return master_dic

def Pickle_Dic(master_dic):
    pickle.dump(master_dic, open(os.path.join(os.getcwd(),"Requisites/referenceDic.p"),mode="wb"))

if __name__ == "__main__":
    master_dic = Comparing_txt()
    Pickle_Dic(master_dic)
    print(pickle.load(open(os.path.join(os.getcwd(),"Requisites/referenceDic.p"),mode="rb")))

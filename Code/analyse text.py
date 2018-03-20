import os
import csv
import pickle
import extraforcsv
import copy


def Comparing_txt():
    name = os.getcwd()
    master_dic = {}
    for filename in os.listdir(os.path.join(name, "Text files"))[:len(os.listdir(os.path.join(name, "Text files")))-1]:
        with open(os.path.join(name, "Text files/{0}".format(filename)), mode='r', errors='ignore') as myfile:
            data = myfile.read().replace('\n', '')
            myfile.close()
            with open(os.path.join(name, "Requisites/Publication_Names.csv"), mode='r', errors='ignore') as csvfile:
                places = csv.DictReader(csvfile)
                places_dict = {}
                for row in places:
                    places_dict[row["NP"]] = row["Title"]
# print(places_dict)
            dic = {}
        for key, title in places_dict.items():
            count = data.count(title)
            if count > 0:
                dic[key] = count
        master_dic[filename[filename.find("NP"):filename.find("NP")+4]] = dic
    print(master_dic)
    return master_dic


def Pickle_Dic(master_dic):
    pickle.dump(master_dic, open(os.path.join(
        os.getcwd(), "Requisites/referenceDic.p"), mode="wb"))


def Make_CSV(master_dic):
    # Creates a csv file in the directory of where the program is opened from.
    # To make it the same directory as this script add os.path[0] + "\" to the title
    with open("csvfile.csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(extraforcsv.Titles)
        for dic in master_dic.items():
            # Deep copy function means that the default line stored in extraforcsv.py is not affected
            new_line = copy.deepcopy(extraforcsv.line)
            new_line["Title"] = dic[0]
            for key, item in dic[1].items():
                new_line[key] = item
            dic_list = []
            # Converts the dictionary used to create the contents of a line into a list
            # Which is then easily exported into the csv format
            for title in extraforcsv.Titles:
                dic_list.append(new_line[title])
            csv_writer.writerow(dic_list)


if __name__ == "__main__":
    master_dic = Comparing_txt()
    Make_CSV(master_dic)
    Pickle_Dic(master_dic)
    print(pickle.load(
        open(os.path.join(os.getcwd(), "Requisites/referenceDic.p"), mode="rb")))

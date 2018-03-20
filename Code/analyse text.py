import os
import csv
import pickle
import extraforcsv
import copy
import PyPDF2
import sys


def Comparing_txt():
    name = sys.path[0]
    name = name[:-4]
    master_dic = {}
    for filename in os.listdir(os.path.join(name, "PDFs"))[:len(os.listdir(os.path.join(name, "PDFs")))-1]:
        print(filename)
        with open(os.path.join(name, "PDFs/{0}".format(filename)), mode='rb') as myfile:
            pdfReader = PyPDF2.PdfFileReader(myfile)
            pages = pdfReader.numPages
            with open(os.path.join(name, "Requisites/Publication_Names.csv"), mode='r', encoding="utf-8") as csvfile:
                places = csv.DictReader(csvfile)
                places_dict = {}
                for row in places:
                    places_dict[row["NP"]] = row["Title"]
# print(places_dict)
            dic = {}
            for index in range(pages):
                print("Page: %d" % index)
                page = pdfReader.getPage(index)
                data = page.extractText()
                for key, title in places_dict.items():
                    spaces = data.count(title)
                    nospaces = data.count(title.replace(" ", ""))
                    if spaces > nospaces:
                        count = spaces
                    else:
                        count = nospaces 
                    if count > 0:
                        for frequency in range(count):
                            if key in dic:
                                dic[key].append(index)
                            else:
                                dic[key] = [index + 1]
        master_dic[filename[filename.find("NP"):filename.find("NP")+4]] = dic
    print(master_dic)
    return master_dic


def Pickle_Dic(master_dic):
    pickle.dump(master_dic, open(os.path.join(
        os.getcwd(), "Requisites/referenceDic.p"), mode="wb"))


def PageRef(master_dic):
    # Creates a csv file in the directory of where the program is opened from.
    # To make it the same directory as this script add os.path[0] + "\" to the title
    with open("PageRef.csv", "w") as csvfile:
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


def Show_Freq(master_dic):
    # Creates a csv file in the directory of where the program is opened from.
    # To make it the same directory as this script add os.path[0] + "\" to the title
    with open("frequencies.csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(extraforcsv.Titles)
        for dic in master_dic.items():
            # Deep copy function means that the default line stored in extraforcsv.py is not affected
            new_line = copy.deepcopy(extraforcsv.line)
            new_line["Title"] = dic[0]
            for key, item in dic[1].items():
                new_line[key] = len(item)
            dic_list = []
            # Converts the dictionary used to create the contents of a line into a list
            # Which is then easily exported into the csv format
            for title in extraforcsv.Titles:
                dic_list.append(new_line[title])
            csv_writer.writerow(dic_list)

            
if __name__ == "__main__":
    master_dic = Comparing_txt()
    PageRef(master_dic)
    Show_Freq(master_dic)
    Pickle_Dic(master_dic)
    print(pickle.load(
        open(os.path.join(os.getcwd(), "Requisites/referenceDic.p"), mode="rb")))

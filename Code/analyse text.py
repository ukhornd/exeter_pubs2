import os
import sys
import copy
import csv
import pickle
import PyPDF2
import extraforcsv


def comparing_txt():
    "Function which uses text files to produce an accurate account of the total references in each book"
    name = os.getcwd()
    master_dic = {}
    for filename in os.listdir(os.path.join(name, "Text files"))[:len(os.listdir(os.path.join(name, "Text files")))]:
        with open(os.path.join(name, "Text files/{0}".format(filename)), mode='r', errors='ignore') as myfile:
            data = myfile.read().replace('\n', '')
            myfile.close()
            with open(os.path.join(name, "Requisites/Publication_Names_txt.csv"), mode='r', errors='ignore') as csvfile:
                places = csv.DictReader(csvfile)
                places_dict = {}
                for row in places:
                    places_dict[row["NP"]] = row["Title"]
            dic = {}
        for key, title in places_dict.items():
            count = data.count(title)
            if count > 0:
                dic[key] = count
        master_dic[filename[filename.find("NP"):filename.find("NP")+4]] = dic
    # print(master_dic)
    return master_dic


def finding_pages():
    "Experimental feature which uses the pdfs to extract which page references are on"
    name = sys.path[0]
    name = name[:-4]
    master_dic = {}
    for filename in os.listdir(os.path.join(name, "PDFs"))[:len(os.listdir(os.path.join(name, "PDFs")))]:
        print(filename)
        with open(os.path.join(name, "PDFs/{0}".format(filename)), mode='rb') as myfile:
            pdfReader = PyPDF2.PdfFileReader(myfile)
            pages = pdfReader.numPages
            with open(os.path.join(name, "Requisites/Publication_Names_PDF.csv"), mode='r', encoding="utf-8") as csvfile:
                places = csv.DictReader(csvfile)
                places_dict = {}
                for row in places:
                    places_dict[row["NP"]] = row["Title"]
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
    # print(master_dic)
    return master_dic


def pickle_dic(master_dic):
    "Saves the nested dictionary to be used by other scripts"
    pickle.dump(master_dic, open(os.path.join(
        os.getcwd(), "Requisites/referenceDic.p"), mode="wb"))




def make_csv(master_dic, contents):
    "Creates a csv file in the directory of the total number of references in each book"
    # To make it the same directory as this script add os.path[0] + "\" to the title
    if contents == "frequencies":
        name = "frequencies.csv"
    elif contents == "pages":
        name = "page_locations.csv"
    with open(name, "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(extraforcsv.Titles)
        for dic in master_dic.items():
            # Deep copy function means that the default line stored in extraforcsv.py is 
            # not affected by adding info
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
    FREQUENCYDIC = comparing_txt()
    PAGESDIC = finding_pages()
    make_csv(FREQUENCYDIC, "frequencies")
    make_csv(PAGESDIC, "pages")
    pickle_dic(FREQUENCYDIC)
    print(pickle.load(
        open(os.path.join(os.getcwd(), "Requisites/referenceDic.p"), mode="rb")))

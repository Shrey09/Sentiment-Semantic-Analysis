import csv
import glob
import re

files=glob.glob("reuters/*.sgm")  # storing names of each reuter file
print(files)
doc_count=0
for file in files:      #opening each file
    f=open(file,"r+")
    data=f.read()
    data=re.compile('<BODY>(.*?)</BODY>',re.DOTALL).findall(data)    # extract data from body tag
    print(data)
    count=0
    for content in data:
        content=content.split("\n")
        content=content[:-2]
        content=" ".join(content)
        count+=1

        with open("reuters_cleaned_2.csv", 'a+',newline='') as csvfile:   # store the extracted document in csv file
            columns=["Documents"]                                         # each row is one document
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            dict={"Documents":content}
            writer.writerow(dict)

    print(count)     # Total body tags in each reuter data file
import re
import codecs
import glob
from itertools import dropwhile
from operator import itemgetter

docs = []
list_rec = []
dict_rec_cc = {}
dict_rec = {}
from os import listdir, chdir, path
chdir("/Users/sandy/PycharmProjects/enrom_sainsbury/maildir")
#names = [d for d in listdir(".") if "." not in d]
names = []
sent_directories = []
word_count = 0
normal_file_count = 0
utf_file_count = 0


def merge_two_dicts_sort(x, y):
    z = x.copy()
    z.update(y)
    return z


def sort_dict(dict):
    getcount = itemgetter(1)
    sorted_invent = sorted(dict.items(), key=getcount)
    return sorted_invent[::-1]

def get_top_emails(x):
    x = x[:100]
    for i in x:
        print(i[0])

for d in listdir("."):
    if "." not in d:
        names.append(d)
print(names)


for name in names :

    chdir("/Users/sandy/PycharmProjects/enrom_sainsbury/maildir/%s" %name)

    sent = glob.glob("*sent*")
    #print(sent)

    for sub_dir in sent:
        # print(sub_dir)
        chdir("/Users/sandy/PycharmProjects/enrom_sainsbury/maildir/%s/%s/" % (name,sub_dir))
        files = listdir(".")
        #print(files)
        for email in files:
            #print(sub_dir,f)
            if '.' in email:
                try:
                    with open(email, 'r') as f:
                        x = f.readlines()
                        parsing = False
                        normal_file_count = normal_file_count +1
                except UnicodeDecodeError:
                    with open(email, 'r', encoding='utf-16-be') as f:
                        x = f.readlines()
                        parsing = False
                        utf_file_count = utf_file_count +1

                for line in x:
                    if line.startswith("X-FileName:"):
                        break
                    if line.startswith("To:"):
                        parsing = True
                    elif line.startswith("Subject"):
                        parsing = False
                    if parsing:
                        line = line.strip("To:")
                        line = line.replace(', ', ',')
                        line = line.strip()
                        line = line.strip(',')
                        line = line.split(',')
                        # print(line)


                        for item in line:
                            # print(item)
                            if item in dict_rec:
                                # print("match")
                                dict_rec[item] = dict_rec[item] + 1.0
                            else:
                                dict_rec[item] = 1.0
                for line in x:
                    if line.startswith("X-FileName:"):
                        break
                    if line.startswith("Cc:"):
                        parsing = True
                    elif line.startswith("Mime"):
                        parsing = False
                    if parsing:
                        line = line.strip("Cc:")
                        line = line.replace(', ', ',')
                        line = line.strip()
                        line = line.strip(',')
                        line = line.split(',')
                        # print(line)
                        for item in line:
                            # print(item)
                            if item in dict_rec_cc:
                                # print("match")
                                dict_rec_cc[item] = dict_rec_cc[item] + .5
                            else:
                                dict_rec_cc[item] = .5
                for line in x:
                    if line in ['\n', '\r\n']:
                        pass

                    else:
                        words = line.strip().split()
                        #print(words)
                        word_count = word_count + len(words)
                        #print(word_count)

print(word_count)
print(normal_file_count)
print(utf_file_count)



final_dic = merge_two_dicts_sort(dict_rec,dict_rec_cc)

sorted_dict = sort_dict(final_dic)

get_top_emails(sorted_dict)


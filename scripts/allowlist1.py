# Removes any lines in the blocklists, that contain domains listed in allow.txt
# Currently not being used

f = open("block.txt", errors="ignore")
list1 = [i.strip() for i in f.readlines()]
f.close()
f = open("allow.txt", errors="ignore")
list2 = [i.strip() for i in f.readlines()]
f.close()
def Diff(list1, list2):
    return list(set(list1) - set(list2)) + list(set(list2) - set(list1))
list1 = Diff(list1, list2)
f = open("block.txt","w")
for i in list1:
    f.write(f"{i}\n")
f.close()

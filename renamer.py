import os

directory = os.listdir("D:\TEMP WORK\Победители 2020\ФОТО СТУДЕНТОВ — копия")

for i in range(len(directory)):
    for_replace = directory[i]
    if "." in for_replace[:len(for_replace)-5]:
        tochka = for_replace.find(".")
        for_replace = for_replace[tochka + 1:]
        
    for_replace = for_replace.replace("   ", " ")
    for_replace = for_replace.replace("  ", " ")
    if for_replace[0] == " ":
        for_replace = for_replace[1:len(for_replace)]
    for_replace = for_replace.title()
    for_replace = for_replace.replace("Jpg", "jpg")
    os.rename("D:\TEMP WORK\Победители 2020\ФОТО СТУДЕНТОВ — копия\\" + directory[i], "D:\Python\\" + for_replace) 
    

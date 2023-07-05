import urllib.request
import json 
import csv
import os

json_file='vacancies_json.txt'
json_file2='employers_json.txt'
csv_file='vacancies.csv'
csv_file2='employers.csv'
per_page=20
page=24
specialization=3

url = "https://api.hh.ru/vacancies?area=16&specialization="+str(specialization)+"&per_page="+str(per_page)
url_company = "https://api.hh.ru/employers/"

f1 = open(csv_file, 'wt', encoding="utf-8")
writer1 = csv.writer(f1)
writer1.writerow(('name', 'requirement', 'responsibility', 'area_name', 'employer_name', 'employer_id'))

f2 = open(csv_file2, 'wt', encoding="utf-8")
writer2 = csv.writer(f2)
writer2.writerow(('name', 'description', 'area_name'))

i = 1
while i <= page:

    # поиск вакансий в регионе с заданой специализацией
    print ("page="+str(i))
    f=open(json_file,'bw')
    request = urllib.request.Request(url+'&page='+str(i))
    response = urllib.request.urlopen(request)
    data = response.read()
    f.write(data)
    f.close()
    i = i + 1
    
    json_data=open(json_file, encoding="utf-8")
    data_vac = json.load(json_data)
    json_data.close()

    # преобразуем json в csv
    n = 0
    found =int (data_vac['found'])
    if found-(i-1)*per_page>per_page:
        vac_per_page=per_page
    else:
        vac_per_page=found-(i-1)*per_page
    
    while n < vac_per_page:
        try:
            name = data_vac['items'][n]['name']
            requirement = data_vac['items'][n]['snippet']['requirement']
            responsibility = data_vac['items'][n]['snippet']['responsibility']
            area_name = data_vac['items'][n]['area']['name']
            employer_name = data_vac['items'][n]['employer']['name']
            employer_id = data_vac['items'][n]['employer']['id']
        except:
            print(">>> Error parsing data, continue...")
        writer1.writerow((name, requirement, responsibility, area_name, employer_name, employer_id))
        print (str(n)+". "+name,"("+employer_name+")")
        n = n + 1

        # получаем подробные сведения о работодателе
        f=open(json_file2,'bw')
        request = urllib.request.Request(url_company+employer_id)
        response = urllib.request.urlopen(request)
        data = response.read()
        f.write(data)
        f.close()

        json_data=open(json_file2, encoding="utf-8")
        data_employers = json.load(json_data)
        json_data.close()

        name = data_employers['name']
        description = data_employers['description']
        area_name = data_employers['area']['name']
        if description is None:
            desc = description
        else:
            desc = description[0:350]
            desc = desc.replace("&quot;", "")
            desc = desc.replace("<strong>", "")
            desc = desc.replace("</strong>", "")
            desc = desc.replace("<p>", "")
            desc = desc.replace("</p>", "")
            desc = desc.replace("<br />", "")
            desc = desc.replace(",", "")
            desc = desc.replace("&nbsp", "")
            desc = desc.replace("<br>", "")	
            desc = desc.replace("</em>", "")
            desc = desc.replace("<em>", "")
            desc = desc.replace("<div>", "")	
            desc = desc.replace("</div>", "")
            desc = desc.replace("</li>", "")	
            desc = desc.replace("<li>", "")
            desc = desc.replace("<ul>", "")	
            desc = desc.replace("</ul>", "")           	
            desc = desc.replace("\n", "")	
            desc = desc.replace("&amp;", "&")
            desc = desc.replace("<ol>", "")
            desc = desc.replace("<span>", "")
            desc = desc.replace("</span>", "")            
        writer2.writerow((name, desc, area_name))

f1.close()
f2.close()


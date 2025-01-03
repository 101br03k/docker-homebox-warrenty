import requests
import json

#headers = {"Authorization": "Bearer XEQOX6ECFH2N3LXYJ2YWBQD62Q"}
#responsehbox = requests.get("https://demo.homebox.software/api/v1/items/export", headers=headers)
##print("printingrespone: ",responsehbox.text)
##print("printingrespone: ",responsehbox.content)
#if responsehbox.status_code == "200":
#    f = open("csv/test1.csv", "w")
#    f.write(responsehbox.text)
#    f.close()


headers2 = {"Authorization": "D3FHTPLVZT6ZIUT7DDL5SOPGXM"}
responsehbox2 = requests.get("http://192.168.0.11:3100/api/v1/items/export", headers=headers2)
print(responsehbox2.status_code)
print("printingrespone: ",responsehbox2.text)
if responsehbox2.status_code == "200":
    g = open("csv/test2.csv", "w")
    g.write(responsehbox2.text)
    g.close()

import io
if responsehbox2.status_code == "200":
    with io.open("csv/test2.csv", "w", encoding="utf-8") as h:
        h.write(responsehbox2.text)
    h.close()

print(type(responsehbox2.text))

#key_expirery = json.loads(responsehbox.text)
#print(key_expirery)
#with io.open("csv/test3.csv", "w", encoding="utf-8") as i:
#    i.write(key_expirery)
#i.close()
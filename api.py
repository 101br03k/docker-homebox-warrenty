# importing the requests library
import requests
import json
import datetime
import string
import io


print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
# api-endpoint
host = "http://192.168.0.11:3100"
URLforbearer = host+"/api/v1/users/login"
URLforexport = host+"/api/v1/items/export"
debug="true"

with open('debug.json') as h:
    js = h.read()
    debug_data = json.loads(js)
    debug = debug_data["debug"]
    h.close()

# opening a file and defining params dict for the parameters to be sent to the API
with open('auth.json') as f:
    js = f.read()
    data = json.loads(js)
    if (debug=="true"):
        print("with open auth.json:",data)
        print()
    f.close()

def getbearer():
    global rbearer_without_bearer, rbearer_expires_at
    # sending get request and saving the response as response object
    print("getting bearer token")
    rbearer = requests.post(url = URLforbearer, auth=('adm-aw@adrie.it', 'Jekomternietin03'), json=data)
    if (rbearer.status_code != 200):
        print("Sorry, something went wrong with the bearer token api.")
        print("status_code:", rbearer.status_code)
        print()
    else:
        rbearer_dict = rbearer.json() #json to dict
        rbearer_without_bearer = rbearer_dict["token"][7:] # number removes x amount of chars from front
        rbearer_expires_at= rbearer_dict["expiresAt"][:21]
        
        if (debug=="true"):
            print(rbearer.json())
            print("status_code:", rbearer.status_code)
            print("rbearer_without_bearer: ",rbearer_without_bearer)
            print(rbearer_expires_at)
            print()

        #format rbearer_expires_at
        rbearer_expires_at_formated = rbearer_expires_at.replace("T", " ") 
        rbearer_dict["bearertokensaved"] = rbearer_without_bearer
        del rbearer_dict["token"]
        del rbearer_dict["attachmentToken"]
        del rbearer_dict["expiresAt"]
        rbearer_dict["expires"] = rbearer_expires_at_formated
        print("rbearer_expires_at_formated",rbearer_expires_at_formated)
        print()
        
        #save rbearerexpiresatformated to file
        i = open("key.json", "w")
        i.write(json.dumps(rbearer_dict))


def auth_and_export():
    print("starting auth_and_export")
    with open('key.json') as g:
        js = g.read()
        key_expirery = json.loads(js)
        bearer_expirery_string = json.dumps(key_expirery["bearertokensaved"])
    class BearerAuth(requests.auth.AuthBase):
        def __init__(self, token):
            print("print bearer_expirery_string:",bearer_expirery_string)
            self.token = bearer_expirery_string
            print("print self.token:",self.token)
        def __call__(self, r):
            r.headers["authorization"] = "Bearer " + self.token
            return r

    headers2 = {"Authorization": "Bearer YOJNDITI5AWHKC4AWMNNJLN4TA"}
    rexport = requests.get(url = URLforexport, headers=headers2)
    #rexport = requests.get(url = URLforexport, auth=BearerAuth('bearer_expirery_string'))

    if (rexport.status_code != 200):
        print("Sorry, something went wrong with the export api.")
        print("status_code:", rexport.status_code)
        print()
    else:
        if (debug=="true"):
            print("status_code:", rexport.status_code)
            print("printingrespone: ",rexport.text)
            print()
        print ("")
        


        #open templates, destenation file and write contents from api and template to destenation
        #with open('templates/header.html') as p:
        #    header = p.read()
        #with open('templates/footer.html') as q:
        #    footer = q.read()
        #with io.open("index.html", "w", encoding="utf-8") as r:
        #    r.write(header)
        #    r.write(rexport.text)
        #    r.write(footer)
        #    r.close()
        #p.close()
        #q.close()


def check_if_bearer_expired():
#load rbearer from file and check if expired
    #get expirery date from file and format
    with open('key.json') as g:
        js = g.read()
        key_expirery = json.loads(js)
        key_expirery_string = json.dumps(key_expirery["expires"])
        key_expirery_string_formatted = key_expirery_string.replace('"', "") 

        #get current date and format
        now = datetime.datetime.now()
        formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')

        if (debug=="true"):
            print('key_expirery["bearertokensaved"]:',key_expirery["bearertokensaved"])
            print('key_expirery["expires"]:',key_expirery["expires"])
            print("formatted_now:",formatted_now)
            print("key_expirery_string_formatted:",key_expirery_string_formatted)
            print()

        #compare current date and expirery date
        if key_expirery_string_formatted > formatted_now:
            if (debug=="true"):
                print("auth key is valid, starting auth_and_export")
                print()
            auth_and_export()
        else:
            if (debug=="true"):
                print("auth key is expirerd, getting new one")
                print()
            getbearer()

check_if_bearer_expired()
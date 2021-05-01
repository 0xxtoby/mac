import requests

url = "https://pan.baidu.com/rest/2.0/xpan/share"


querystring = {"method":"transfer","access_token":"123","shareid":"3440411579","from":"3389535607"}


payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=&quot;sekey&quot;\r\n\r\nS3l2qkR0bI3GUR2UXVVKyRXrm2760dC6mg2ExG0qbUM=\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=&quot;fsidlist&quot;\r\n\r\n[689582071279227,523224362330193]\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=&quot;path&quot;\r\n\r\n/baidu\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'User-Agent': "pan.baidu.com",
    'Referer': "pan.baidu.com",
    'cache-control': "no-cache",
    'Postman-Token': "2756bf0a-adbe-46fe-a305-a84a706052b3"
    }


response = requests.request("POST", url, data=payload, headers=headers, params=querystring)


print(response.text)
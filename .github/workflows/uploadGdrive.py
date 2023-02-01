import json
import requests

headers = {
    "Authorization": "Bearer ya29.a0AVvZVsp96EcPXS2tNEym45jPROX9dZiZnZrDernfk5eFm3bpHRzt_7a6Ybwdwjgsic4Q5qMhb5Vw4Mc9ZPTYV1wvgNmJ0uVTy5xUPJp6QDOrNERBEY19IL9GTvZdFC0nF65-TpDsiohczro1eRUaDidFHXPYaCgYKAbsSARISFQGbdwaIfTw4I6gcnzd9itcs8U3YNg0163"
}
params = {
    "name": "testz1231asdasdas2z",
    "mimeType": "text/plain"
}
files = {
    "data": ("metadata", json.dumps(params), "application/json;charset=UTF-8"),
    "file": open("./test.txt", "rb")
}

response = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart", headers=headers, files=files)

print(response.text)

import json
import requests
import os

token = os.environ.get("OAUTH_GOOGLE")
headers = {
    "Authorization": "Bearer {}".format(token)
}
params = {
    "name": "test_apk",
    "mimeType": "application/vnd.android.package-archive"
}
files = {
    "data": ("metadata", json.dumps(params), "application/json;charset=UTF-8"),
    "file": open("build/app/outputs/flutter-apk/app-release.apk", "rb")
}

response = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart", headers=headers, files=files)

print(response.text)

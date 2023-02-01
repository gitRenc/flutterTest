import json
import requests
import os

token = os.environ.get("OAUTH_GOOGLE")
print(token)
headers = {
    "Authorization": "Bearer {}".format(token)
}
# params = {
#     "name": "test_apk",
#     "mimeType": "application/vnd.android.package-archive"
# }
# files = {
#     "data": ("metadata", json.dumps(params), "application/json;charset=UTF-8"),
#     "file": open("build/app/outputs/flutter-apk/app-release.apk", "rb")
# }
params = {
    "name": "testtttt",
    "mimeType": "plain/text"
}
files = {
    "data": ("metadata", json.dumps(params), "application/json;charset=UTF-8"),
    "file": open("./test.txt", "rb")
}
response = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart", headers=headers, files=files)


json_data = json.loads(response.text)
# link = 'https://drive.google.com/file/d/{}/view'.format(json_data["id"])
print(json_data)

# with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
#     print(f'link={link}', file=fh)

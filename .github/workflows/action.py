import os
import requests
import json
import asyncio
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta, timezone


async def getGithubMerged():
    baseUrl = "https://api.github.com/search/issues"
    owner = "gitRenc"
    repo = "flutterTest"

    # time in UTC
    # 18.00 utc = 02.00 wita
    startDate = datetime.now(timezone.utc) - timedelta(hours=24)
    endDate = datetime.now(timezone.utc)

    url = "{}?q=repo:{}/{}+is:pr+is:merged+merged:{}..{}".format(
        baseUrl, owner, repo, startDate.strftime("%Y-%m-%dT%H:%M"), endDate.strftime("%Y-%m-%dT%H:%M"))

    try:
        response = requests.get(url)
        json_data = json.loads(response.text)
        titles = ()
        for item in json_data['items']:
            temp = list(titles)
            temp.append(item["title"])
            titles = tuple(temp)
        return titles
    except:
        return "github Api failed"


async def getJiraIssues():
    #
    # token link : https://id.atlassian.com/manage-profile/security/api-tokens
    #
    baseUrl = "https://richtesting.atlassian.net/rest/api/3/search"
    token = os.environ.get("JIRA_TOKEN")
    email = "richbytesting@gmail.com"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    issues = []
    titles = await getGithubMerged()

    # query for jira request
    params = {
        "field": "status",
        # "project": projectKey
        "jql": ""
    }

    try:
        if len(titles) > 0:
            for items in titles:
                params["jql"] = "key in " + ("(" + ",".join(titles) + ")")

        else:
            return ("no issues")
        url = "{}".format(baseUrl)
        response = requests.get(url, headers=headers, auth=auth, params=params)
        if (response.status_code == 200):
            json_data = json.loads(response.text)
            for data in json_data["issues"]:
                issues.append({
                    "title": data["key"],
                    "status": data["fields"]["status"]["name"]
                })
    except:
        return ("Jira Api failed")
    return (issues)


async def postTeams():
    url = "https://ptwolkkclouddevelopment.webhook.office.com/webhookb2/cfa586db-88e3-4755-b058-579cc7ac7927@509671eb-b559-459a-87f0-5635b2ec0f07/IncomingWebhook/1abc1617584648dc908146d794fd4a94/645af85f-a16e-4d30-9f7a-bf0ca707c61e"
    headers = {
        "Content-Type": "application/json",
    }

    issues = await getJiraIssues()
    issuesString = ""
    startDate = datetime.now(timezone.utc) - timedelta(hours=24)
    endDate = datetime.now(timezone.utc)
    startDateFormated = startDate.strftime("%Y-%m-%d")
    endDateFormated = endDate.strftime("%Y-%m-%d")
    if (len(issues) > 0):
        for x in issues:
            x = "- {} - {}\n".format(x["title"], x["status"])
            issuesString += x
    content = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "medium",
                            "weight": "bolder",
                            "text": "Jira Issues"
                        },
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "type": "Column",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "spacing": "None",
                                            "text": "From : {}".format(startDateFormated),
                                            "isSubtle": "true",
                                            "wrap": "true"
                                        },
                                        {
                                            "type": "TextBlock",
                                            "spacing": "None",
                                            "text": "To: {}".format(endDateFormated),
                                            "isSubtle": "true",
                                            "wrap": "true"
                                        }
                                    ],
                                    "width": "stretch"
                                }
                            ]
                        },
                        {
                            "type": "TextBlock",
                            "text": "{}".format(issuesString),
                            "wrap": "true"
                        },
                        {
                            "type": "TextBlock",
                            "text": "latest build : halo",
                            "wrap": "true"
                        }
                    ],
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.5"
                }
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=content)
        print(response)
    except:
        print("teams api failed")

    return "haha"


async def main():
    # print(await postTeams())
    print(await(getJiraIssues()))


asyncio.run(main())

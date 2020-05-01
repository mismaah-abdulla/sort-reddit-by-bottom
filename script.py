import requests
import json
import concurrent.futures
import time
import os

def getMoreComments(unsortedComments, threadLink, commentID):
    url = f'https://reddit.com{threadLink}{commentID}.json'
    print(f'Fetching comments {commentID}')
    resp = requests.get(url, headers = {'User-agent': 'lol'})
    if resp.ok:
        data = resp.json()[1]["data"]["children"]
        if data:
            if data[0]["kind"] == "t1":
                comment = data[0]["data"]
                c = {
                    "text": comment["body"],
                    "user": comment["author"],
                    "score": comment["score"],
                    "permalink": f'https://reddit.com{comment["permalink"]}'
                }
                unsortedComments.append(c)

print("Enter reddit thread url: ")
try:
    url = input()
    url = url+'.json'
    resp = requests.get(url, headers = {'User-agent': 'lol'})
    if resp.ok:
        data = resp.json()
        threadLink = data[0]["data"]["children"][0]["data"]["permalink"]
        threadTitle = data[0]["data"]["children"][0]["data"]["title"]
        allComments = data[1]["data"]["children"]
        unsortedComments = []
        for i in allComments:
            if i["kind"] == "t1":
                comment = i["data"]
                c = {
                    "text": comment["body"],
                    "user": comment["author"],
                    "score": comment["score"],
                    "permalink": f'https://reddit.com{comment["permalink"]}'
                }
                unsortedComments.append(c)
            elif i["kind"] == "more":
                commentIDs = []
                for j in i["data"]["children"]:
                    commentIDs.append(j)
                with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                    futures = {executor.submit(getMoreComments, unsortedComments, threadLink, i): i for i in commentIDs}
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            data = future.result()
                        except Exception as e:
                            print(e)
        sortedComments = sorted(unsortedComments, key=lambda k: k['score'])
        # Uncomment to get results as json file
        # with open("results.json", "w") as f:
        #     json.dump(sortedComments, f)
        with open("index.html", "w", encoding="utf-8") as f:
            html = f'''<!DOCTYPE html>
            <head></head>
            <body>
            <style>.comment {{margin: 30px 50px 30px;}}
            h1 {{margin: 10px 25px 10px;}} 
            .divider {{border-top: 1px solid #bbb;}}
            p {{margin-block-start: 0px;
            margin-block-end: 0px;}}
            .top {{font-size:12px}}
            body {{font-family: 'Helvetica', 'Arial', sans-serif;}}</style>
            <div>
            <h1><a href="https://reddit.com{threadLink}">{threadTitle}</a></h1>
            <div class="comment">'''
            for i in sortedComments:
                html = html + f'''<p class="top"><b>{i["user"]}</b> {i["score"]} points <a href="{i["permalink"]}">permalink</a></p>
                <p>{i["text"]}</p>
                <hr class="divider">'''
            html = html + "</div></div></body>"
            f.write(html)
        print("Complete. Results saved in index.html")
        os.system("start " + "index.html")
    else:
        print(resp.status_code)
except:
    print("Invalid. Exiting...")
    time.sleep(5)
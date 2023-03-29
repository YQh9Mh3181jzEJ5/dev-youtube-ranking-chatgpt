from flask import Flask, render_template
import requests
import openai
import os

app = Flask(__name__, static_folder='html/static', template_folder='html/templates')

def read_api_key(key_name: str) -> str:
    """
    環境変数からAPIキーを読み込む
    """
    key = os.environ.get(key_name)
    if key is None:
        raise ValueError(f"{key_name} is not set in environment variables")
    return key

# YouTube APIキーを読み込む
YOUTUBE_API_KEY = read_api_key('AIzaSyDPYbo0Bq9sYghh2UVc_k0JNkpLtUfJv0M')

# OpenAI APIキーを読み込む
OPENAI_API_KEY = read_api_key('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')
openai.api_key = OPENAI_API_KEY

@app.route("/")
def index():
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/videos",
        {
            "params": {
                "part": "snippet",
                "chart": "mostPopular",
                "maxResults": 3,
                "regionCode": "JP",
                "key": YOUTUBE_API_KEY,
            }
        },
    )

    videos = []
    for item in response.json()["items"]:
        video = {
            "title": item["snippet"]["title"],
            "url": "https://www.youtube.com/watch?v=" + item["id"],
        }
        videos.append(video)

    summaries = []
    for video in videos:
        prompt = "要約: " + video["title"]
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=40,
        )
        summary = response.choices[0].text.strip()
        summaries.append(summary)

    return render_template("index.html", videos=videos, summaries=summaries)

@app.route("/daily")
def daily():
    return render_template("daily.html")

if __name__ == "__main__":
    app.run(debug=True)

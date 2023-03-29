const openai = require("openai");
const fetch = require("node-fetch");

const os = require("os");

const read_api_key = (key_name) => {
  const key = os.environ.get(key_name);
  if (key === undefined) {
    throw new Error(key_name + " is not set in environment variables");
  }
  return key;
};

const YOUTUBE_API_KEY = read_api_key("AIzaSyDPYbo0Bq9sYghh2UVc_k0JNkpLtUfJv0M");
const OPENAI_API_KEY = read_api_key("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");
openai.api_key = OPENAI_API_KEY;

const app = require("express")();

app.get("/", async (req, res) => {
  const response = await fetch(
    "https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&maxResults=3&regionCode=JP&key=" +
      YOUTUBE_API_KEY
  );
  const json = await response.json();

  const videos = [];
  json.items.forEach((item) => {
    const video = {
      title: item.snippet.title,
      url: "https://www.youtube.com/watch?v=" + item.id,
    };
    videos.push(video);
  });

  const summaries = [];
  for (const video of videos) {
    const prompt = "要約: " + video.title;
    const response = await openai.Completion.create({
      engine: "davinci",
      prompt: prompt,
      max_tokens: 40,
    });
    const summary = response.choices[0].text.trim();
    summaries.push(summary);
  }

  res.render("index.html", { videos: videos, summaries: summaries });
});

app.get("/daily", (req, res) => {
  res.render("daily.html");
});

app.listen(process.env.PORT || 3000);

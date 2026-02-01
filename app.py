from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# Ensure folder exists
if not os.path.exists("saved_posts"):
    os.makedirs("saved_posts")

PLATFORMS = ["TikTok", "Instagram", "X", "YouTube", "WhatsApp", "Facebook", "Snapchat", "LinkedIn"]

# Simulate platform-specific content adaptation
def adapt_content(content, platform_name):
    adapted = content.copy()
    if platform_name.lower() == "x":
        adapted['text'] = adapted['text'][:280]
    if platform_name.lower() == "instagram":
        adapted['hashtags'] = adapted.get('hashtags', [])[:5]
    if platform_name.lower() == "linkedin":
        adapted['hashtags'] = []
    return adapted

@app.route("/")
def index():
    return render_template("index.html", platforms=PLATFORMS)

@app.route("/post", methods=["POST"])
def post_content():
    data = request.json
    text = data.get("text", "")
    hashtags = data.get("hashtags", [])
    media = data.get("media", [])
    selected_platforms = data.get("platforms", [])

    results = []
    post_data = {
        "text": text,
        "hashtags": hashtags,
        "media": media,
        "timestamp": str(datetime.now()),
        "platforms": selected_platforms
    }

    # Save locally
    filename = f"saved_posts/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(post_data, f, indent=4)

    # Simulate posting
    for platform in selected_platforms:
        adapted = adapt_content(post_data, platform)
        results.append({
            "platform": platform,
            "text": adapted['text'],
            "hashtags": adapted.get('hashtags', []),
            "media": adapted.get('media', [])
        })

    return jsonify({"status": "success", "results": results, "filename": filename})

if __name__ == "__main__":
    app.run(debug=True)

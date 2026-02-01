const form = document.getElementById("postForm");
const output = document.getElementById("output");
const downloadBtn = document.getElementById("downloadBtn");

let allPosts = [];

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const text = document.getElementById("text").value;
    const hashtags = document.getElementById("hashtags").value.split(",").map(h => h.trim()).filter(h => h);
    const media = document.getElementById("media").value.split(",").map(m => m.trim()).filter(m => m);
    const platforms = Array.from(document.querySelectorAll('input[name="platform"]:checked')).map(cb => cb.value);

    if (!text || platforms.length === 0) {
        alert("Please enter text and select at least one platform.");
        return;
    }

    const response = await fetch("/post", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text, hashtags, media, platforms})
    });

    const data = await response.json();
    if (data.status === "success") {
        allPosts.push(data);
        output.textContent = "";
        data.results.forEach(res => {
            output.textContent += `[${res.platform}] Posting...\nText: ${res.text}\nHashtags: ${res.hashtags.join(", ")}\nMedia: ${res.media.join(", ")}\nPost successful!\n\n`;
        });
    }
});

// Download all posts as JSON
downloadBtn.addEventListener("click", () => {
    const blob = new Blob([JSON.stringify(allPosts, null, 4)], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "all_posts.json";
    a.click();
    URL.revokeObjectURL(url);
});

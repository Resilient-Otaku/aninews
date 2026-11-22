
from flask import Flask, render_template_string, jsonify, request
import json
import urllib.request
import urllib.parse

app = Flask(__name__)
@app.route("/api/anime")
def get_anime():
    query = request.args.get("q", "").strip()

    if query:
        params = urllib.parse.urlencode({
            "q": query,
            "limit": 12,
            "sfw": "true"
        })
        url = "https://api.tenrai.org/v1/anime?" + params
    else:
        url = "https://api.tenrai.org/v1/top/anime?limit=12&sfw=true"

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Aninews/1.0"}
        )

        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))

        return jsonify(data)

    except Exception as error:
        return jsonify({"error": str(error)}), 503
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Aninews</title>

<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    background: #080b18;
    color: white;
    font-family: Arial, sans-serif;
}
header {
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #10152a;
    border-bottom: 1px solid #292b50;
}
.logo {
    color: #b58aff;
    font-size: 25px;
    font-weight: bold;
}
nav {
    display: flex;
    gap: 10px;
    padding: 12px;
    overflow-x: auto;
    background: #10152a;
}
nav button, .genre {
    background: #202746;
    color: white;
    border: 1px solid #444b75;
    padding: 10px 15px;
    border-radius: 20px;
    white-space: nowrap;
}
button { cursor: pointer; }
nav button:hover, .genre:hover {
    background: #783ce5;
}
main { padding: 20px; }
.hero {
    padding: 28px 20px;
    border-radius: 20px;
    background: linear-gradient(120deg,#6026a9,#174db5);
    margin-bottom: 25px;
}
.hero h1 { font-size: 30px; }
.hero p { color: #e0ddff; }
h2 { color: #c5a5ff; }
.search {
    width: 100%;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #454b77;
    background: #151b32;
    color: white;
    font-size: 16px;
    margin: 10px 0 15px;
}
.genres {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 5px 0 15px;
}
.anime-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit,minmax(145px,1fr));
    gap: 15px;
}
.card {
    background: #141b33;
    border: 1px solid #30395d;
    border-radius: 15px;
    overflow: hidden;
}
.poster {
    height: 145px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 48px;
    background: linear-gradient(145deg,#7135bd,#1465a9);
}
.card:nth-child(2n) .poster {
    background: linear-gradient(145deg,#b43d87,#4934a5);
}
.card:nth-child(3n) .poster {
    background: linear-gradient(145deg,#146d87,#303b9b);
}
.info { padding: 12px; }
.info h3 { margin: 0 0 8px; font-size: 16px; }
.info p { color: #aeb8d5; font-size: 12px; }
.tag {
    color: #c9aaff;
    font-size: 12px;
}
.section { margin-top: 30px; }
.panel {
    background: #141b33;
    padding: 18px;
    border-radius: 15px;
    margin-top: 12px;
}
.page { display: none; }
.page.active { display: block; }
.chat-input {
    width: 100%;
    padding: 13px;
    border-radius: 10px;
    background: #202746;
    color: white;
    border: 1px solid #555b80;
}
footer {
    text-align: center;
    padding: 25px;
    color: #8d96b7;
    font-size: 12px;
}
.carousel {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 15px;
}

.carousel-window {
    flex: 1;
    overflow: hidden;
    min-width: 0;
}

.carousel-track {
    display: flex;
    gap: 15px;
    transition: transform 0.55s ease;
    will-change: transform;
}

.carousel-track .card {
    flex: 0 0 180px;
    min-width: 0;
    transition: box-shadow 0.4s, border-color 0.4s;
}

.carousel-track .card:nth-child(4n+1) {
    border-color: #a855f7;
    box-shadow: 0 0 12px #9333ea55;
}

.carousel-track .card:nth-child(4n+2) {
    border-color: #3b82f6;
    box-shadow: 0 0 12px #2563eb55;
}

.carousel-track .card:nth-child(4n+3) {
    border-color: #06b6d4;
    box-shadow: 0 0 12px #06b6d455;
}

.carousel-track .card:nth-child(4n+4) {
    border-color: #ec4899;
    box-shadow: 0 0 12px #ec489955;
}

.arrow {
    background: #29204e;
    color: white;
    border: 1px solid #a78bfa;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    flex-shrink: 0;
    font-size: 17px;
}
</style>
</head>

<body>

<header>
    <div class="logo">🌌 ANINEWS</div>
    <div>Animeverse</div>
</header>

<nav>
    <button onclick="showPage('home')">🏠 Home</button>
    <button onclick="showPage('explore')">🔍 Explore</button>
    <button onclick="showPage('news')">📰 News</button>
    <button onclick="showPage('bot')">🤖 AniBot</button>
    <button onclick="showPage('settings')">⚙️ Settings</button>
</nav>

<main>

<section id="home" class="page active">
    <div class="hero">
        <h1>Welcome to Aninews!</h1>
        <p>Your personal gateway to the anime universe.</p>
        <button class="genre" onclick="showPage('explore')">
            Explore Anime →
        </button>
    </div>

    <h2>🔥 Trending Anime</h2>
    <div class="carousel">
    <button class="arrow" onclick="slideAnime(-1)">❮</button>

    <div class="carousel-window" id="carouselWindow">
        <div class="carousel-track" id="homeGrid"></div>
    </div>

    <button class="arrow" onclick="slideAnime(1)">❯</button>
</div>
</section>

<section id="explore" class="page">
    <h2>🔍 Explore Anime</h2>
    <input class="search" id="search"
    placeholder="Search your favourite anime..."
    oninput="filterAnime()">

    <div class="genres">
        <button class="genre" onclick="setGenre('All')">All</button>
        <button class="genre" onclick="setGenre('Action')">Action</button>
        <button class="genre" onclick="setGenre('Romance')">Romance</button>
        <button class="genre" onclick="setGenre('Fantasy')">Fantasy</button>
        <button class="genre" onclick="setGenre('Sports')">Sports</button>
        <button class="genre" onclick="setGenre('Mystery')">Mystery</button>
    </div>

    <div class="anime-grid" id="exploreGrid"></div>
</section>

<section id="news" class="page">
    <h2>📰 Anime News</h2>
    <div class="panel">
        <h3>Welcome to Anime News!</h3>
        <p>Anime announcements and release updates will appear here.</p>
        <small>Demo section — live news is not connected yet.</small>
    </div>
</section>

<section id="bot" class="page">
    <h2>🤖 AniBot</h2>
    <div class="panel">
        <p>Welcome! I'm AniBot, your anime assistant.</p>
        <p id="reply">Ask me about anime!</p>
        <input class="chat-input" id="question"
        placeholder="Ask something about anime...">
        <br><br>
        <button class="genre" onclick="askBot()">Send message</button>
    </div>
</section>

<section id="settings" class="page">
    <h2>⚙️ Settings</h2>
    <div class="panel">
        <p>🌌 Theme: Dark futuristic</p>
        <p>💜 Accent: Purple and blue</p>
        <p>Version: Aninews 2.0</p>
    </div>
</section>

</main>

<footer>ANINEWS © 2026 | Discover. Explore. Connect.</footer>

<script>
let anime = [];
async function loadAnime() {
    try {
        const response = await fetch("/api/anime");
        const result = await response.json();

        if (result.error) {
            throw new Error(result.error);
        }

        anime = result.data || [];

        document.getElementById("homeGrid").innerHTML =
            createCards(anime);

        filterAnime();

    } catch (error) {
        console.error("Anime loading failed:", error);
        document.getElementById("homeGrid").innerHTML =
            "<p>Unable to load anime. Please refresh.</p>";
    }
}

loadAnime();
let selectedGenre = "All";
let carouselIndex = 0;

function slideAnime(direction) {
    const track = document.getElementById("homeGrid");
    const cards = track.querySelectorAll(".card");

    if (cards.length === 0) return;

    const cardWidth = cards[0].offsetWidth + 15;
    const visibleCards = Math.max(
        1,
        Math.floor(track.parentElement.offsetWidth / cardWidth)
    );

    const maxIndex = Math.max(0, cards.length - visibleCards);

    carouselIndex = Math.max(
        0,
        Math.min(maxIndex, carouselIndex + direction)
    );

    track.style.transform =
        `translateX(-${carouselIndex * cardWidth}px)`;

    playWhoosh();
}
function playWhoosh() {
    try {
        const AudioContext =
            window.AudioContext || window.webkitAudioContext;

        const audio = new AudioContext();
        const oscillator = audio.createOscillator();
        const gain = audio.createGain();

        oscillator.type = "sawtooth";
        oscillator.frequency.setValueAtTime(500, audio.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(
            100, audio.currentTime + 0.25
        );

        gain.gain.setValueAtTime(0.08, audio.currentTime);
        gain.gain.exponentialRampToValueAtTime(
            0.001, audio.currentTime + 0.25
        );

        oscillator.connect(gain);
        gain.connect(audio.destination);

        oscillator.start();
        oscillator.stop(audio.currentTime + 0.25);

        oscillator.onended = () => audio.close();
    } catch (error) {
        console.log("Sound unavailable");
    }
}
function createCards(list) {
    return list.map(a => `
        <div class="card">
            <div class="poster">
                <img src="${a.images?.jpg?.large_image_url || a.images?.jpg?.image_url || ''}"
                     alt="${a.title_english || a.title}"
                     style="width:100%;height:100%;object-fit:cover;border-radius:12px;">
            </div>

            <div class="info">
                <h3>${a.title_english || a.title}</h3>
                <span class="tag">
                    ${a.genres?.map(g => g.name).slice(0, 2).join(" • ") || "Anime"}
                </span>
                <p>⭐ ${a.score || "N/A"}</p>
            </div>
        </div>
    `).join("");
}

function filterAnime() {
    const q = document.getElementById("search").value.toLowerCase();

    const results = anime.filter(a => {
        const title = (a.title_english || a.title || "").toLowerCase();

        const genres = (a.genres || []).map(g => g.name);

        return title.includes(q) &&
            (selectedGenre === "All" || genres.includes(selectedGenre));
    });

    document.getElementById("exploreGrid").innerHTML =
        results.length ? createCards(results) : "<p>No anime found.</p>";
}

function setGenre(genre) {
 selectedGenre = genre;
 filterAnime();
}

function showPage(id) {
 document.querySelectorAll(".page").forEach(p =>
   p.classList.remove("active")
 );
 document.getElementById(id).classList.add("active");
 if(id === "explore") filterAnime();
}

function askBot() {
 const q = document.getElementById("question").value.trim();
 if(!q) return;
 document.getElementById("reply").innerText =
 "AniBot: I'm currently a demo assistant. Real AI chat is coming soon!";
 document.getElementById("question").value = "";
}

document.getElementById("homeGrid").innerHTML =
 createCards(anime)
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run()

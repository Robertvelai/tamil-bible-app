
let timerId = null;
let currentMinutes = 5;

function updateClock() {
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const time = now.toLocaleTimeString('ta-IN');
    const date = now.toLocaleDateString('ta-IN', options);
    document.getElementById("datetime").innerText = `${date} - ${time}`;
}
setInterval(updateClock, 1000);
updateClock();

function speakTamil(text) {
    const voices = speechSynthesis.getVoices();
    const tamilVoice = voices.find(v => v.lang === 'ta-IN' || v.name.includes("Tamil"));
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ta-IN';
    if (tamilVoice) utterance.voice = tamilVoice;
    utterance.rate = 0.9;
    speechSynthesis.speak(utterance);
}

function fetchVerses() {
    fetch('/verses')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('verseList');
            list.innerHTML = '';
            data.forEach((verse, i) => {
                list.innerHTML += `
                    <li>
                        ${verse}
                    </li>
                `;
            });
        });
}

function addVerse() {
    const verse = document.getElementById('newVerse').value.trim();
    if (!verse) return alert("வசனம் எழுதவும்");
    const formData = new FormData();
    formData.append('verse', verse);
    fetch('/add', { method: 'POST', body: formData })
        .then(() => {
            document.getElementById('newVerse').value = '';
            fetchVerses();
        });
}

function updateTimeLabel(value) {
    currentMinutes = parseInt(value);
    document.getElementById('timeLabel').innerText = `${value} நிமிடம்`;
}

function startVerseRotation() {
    clearInterval(timerId);
    showRandomVerse();
    timerId = setInterval(showRandomVerse, currentMinutes * 60000);
}

function showRandomVerse() {
    fetch('/verses')
        .then(res => res.json())
        .then(data => {
            if (data.length > 0) {
                const verse = data[Math.floor(Math.random() * data.length)];
                document.getElementById('verseDisplay').innerText = verse;
                speakTamil(verse);
            }
        });
}

function startDictation() {
    if (!('webkitSpeechRecognition' in window)) {
        alert("உங்கள் browser வாய்மொழி அடையாளம் செய்ய முடியவில்லை.");
        return;
    }
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'ta-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.onresult = function(event) {
        const speechResult = event.results[0][0].transcript;
        document.getElementById('newVerse').value = speechResult;
    };
    recognition.start();
}

window.onload = fetchVerses;

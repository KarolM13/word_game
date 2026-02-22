let currentGameId = null;
let wordLength = 0;
let currentCategory = "";
let currentMode = null;
let currentStreak = 0;
let currentNick = "";

function showMenu() {
    document.getElementById("menu").classList.remove("hidden");
    document.getElementById("game").classList.add("hidden");
    document.getElementById("nickScreen").classList.add("hidden");
    loadLeaderboard();
}

function showGame() {
    document.getElementById("menu").classList.add("hidden");
    document.getElementById("game").classList.remove("hidden");
    document.getElementById("nickScreen").classList.add("hidden");
}

function showNickScreen() {
    document.getElementById("menu").classList.add("hidden");
    document.getElementById("game").classList.add("hidden");
    document.getElementById("nickScreen").classList.remove("hidden");
}

function loadLeaderboard() {
    fetch("/api/leaderboard")
        .then(r => r.json())
        .then(data => {
            const tbody = document.getElementById("leaderboardBody");
            tbody.innerHTML = "";
            if (!data.length) {
                tbody.innerHTML = "<tr><td colspan='3'>No scores yet</td></tr>";
                return;
            }
            data.forEach((score, index) => {
                const row = document.createElement("tr");
                row.innerHTML = `<td>${index + 1}</td><td>${score.nick}</td><td>${score.streak}</td>`;
                tbody.appendChild(row);
            });
        })
        .catch(err => console.error("Error loading leaderboard:", err));
}

function startDaily() {
    const today = new Date().toISOString().split("T")[0];
    currentMode = "daily";
    showGame();
    document.getElementById("board").innerHTML = "";
    document.getElementById("streakCounter").classList.add("hidden");
    document.getElementById("nextWordBtn").classList.add("hidden");
    document.getElementById("info").textContent = "";

    if (localStorage.getItem("dailyPlayed") === today) {
        document.getElementById("info").textContent = "You already played today! Come back tomorrow.";
        document.getElementById("guessBtn").classList.add("hidden");
        document.getElementById("guess").classList.add("hidden");
        return;
    }

    document.getElementById("guess").classList.remove("hidden");
    document.getElementById("guessBtn").classList.remove("hidden");

    fetch("/api/daily")
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                document.getElementById("info").textContent = data.error;
                return;
            }
            currentGameId = data.game_id;
            wordLength = data.word_length;
            currentCategory = data.category;
            const input = document.getElementById("guess");
            input.maxLength = wordLength;
            input.placeholder = "─".repeat(wordLength);
            updateInfo(data.max_attempts);
        })
        .catch(err => console.error("Error starting daily:", err));
}

function startStreak(nick) {
    currentMode = "streak";
    currentNick = nick;
    currentStreak = 0;
    showGame();
    document.getElementById("board").innerHTML = "";
    document.getElementById("info").textContent = "";
    document.getElementById("guess").classList.remove("hidden");
    document.getElementById("guessBtn").classList.remove("hidden");
    document.getElementById("nextWordBtn").classList.add("hidden");

    const streakCounter = document.getElementById("streakCounter");
    streakCounter.classList.remove("hidden");
    streakCounter.textContent = `Streak: ${currentStreak}`;

    fetch(`/api/streak/start?nick=${encodeURIComponent(nick)}`)
        .then(r => r.json())
        .then(data => {
            if (data.error) { alert(data.error); showMenu(); return; }
            currentGameId = data.game_id;
            wordLength = data.word_length;
            currentCategory = data.category;
            const input = document.getElementById("guess");
            input.maxLength = wordLength;
            input.placeholder = "─".repeat(wordLength);
            updateInfo(data.max_attempts);
        })
        .catch(err => console.error("Error starting streak:", err));
}

function nextStreakWord() {
    document.getElementById("board").innerHTML = "";
    document.getElementById("info").textContent = "";
    document.getElementById("guess").value = "";
    document.getElementById("nextWordBtn").classList.add("hidden");
    document.getElementById("guess").classList.remove("hidden");
    document.getElementById("guessBtn").classList.remove("hidden");

    fetch(`/api/streak/next?game_id=${currentGameId}`)
        .then(r => r.json())
        .then(data => {
            if (data.error) { alert(data.error); showMenu(); return; }
            currentGameId = data.game_id;
            wordLength = data.word_length;
            currentCategory = data.category;
            const input = document.getElementById("guess");
            input.maxLength = wordLength;
            input.placeholder = "─".repeat(wordLength);
            updateInfo(data.max_attempts);
        })
        .catch(err => console.error("Error loading next word:", err));
}

function updateInfo(remaining) {
    document.getElementById("info").textContent =
        `Category: ${currentCategory} | Letters: ${wordLength} | Attempts left: ${remaining}`;
}

document.getElementById("guessBtn").addEventListener("click", function () {
    const guessValue = document.getElementById("guess").value.trim();
    if (!currentGameId) { alert("No active game!"); return; }
    if (!guessValue) { alert("Enter a word!"); return; }
    if (guessValue.length !== wordLength) {
        alert(`Word must be exactly ${wordLength} letters!`);
        return;
    }

    fetch("/api/guess", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ guess: guessValue, game_id: currentGameId })
    })
        .then(r => r.json())
        .then(data => {
            if (data.error) { alert(data.error); return; }

            const board = document.getElementById("board");
            const row = document.createElement("div");
            row.classList.add("guess-row");
            data.result.forEach((color, i) => {
                const letter = document.createElement("span");
                letter.textContent = guessValue[i].toUpperCase();
                letter.classList.add(color);
                row.appendChild(letter);
            });
            board.appendChild(row);

            if (data.is_won) {
                confetti({
                    particleCount:100,
                    spread: 70,
                    origin: {y:0.6}
                });
                if (currentMode === "streak") {
                    currentStreak = data.streak;
                    document.getElementById("streakCounter").textContent = `Streak: ${currentStreak}`;
                    const msg = document.createElement("p");
                    msg.textContent = `✅ Correct! Streak: ${currentStreak}`;
                    msg.classList.add("message", "win");
                    board.appendChild(msg);
                    document.getElementById("guess").classList.add("hidden");
                    document.getElementById("guessBtn").classList.add("hidden");
                    document.getElementById("nextWordBtn").classList.remove("hidden");
                } else {
                    localStorage.setItem("dailyPlayed", new Date().toISOString().split("T")[0]);
                    const msg = document.createElement("p");
                    msg.textContent = "🎉 Congratulations! You won!";
                    msg.classList.add("message", "win");
                    board.appendChild(msg);
                    document.getElementById("guess").classList.add("hidden");
                    document.getElementById("guessBtn").classList.add("hidden");
                    currentGameId = null;
                }
            } else if (data.is_over) {
                const msg = document.createElement("p");
                if (currentMode === "streak") {
                    msg.textContent = ` Game over! The word was: "${data.answer.toUpperCase()}" | Final streak: ${currentStreak}`;
                    loadLeaderboard();
                } else {
                    msg.textContent = ` Game over! The word was: "${data.answer.toUpperCase()}"`;
                }
                msg.classList.add("message", "lose");
                board.appendChild(msg);
                document.getElementById("guess").classList.add("hidden");
                document.getElementById("guessBtn").classList.add("hidden");
                currentGameId = null;
            } else {
                updateInfo(data.remaining);
            }

            document.getElementById("guess").value = "";
        })
        .catch(err => console.error("Error:", err));
});

document.getElementById("nextWordBtn").addEventListener("click", nextStreakWord);
document.getElementById("dailyBtn").addEventListener("click", startDaily);
document.getElementById("streakBtn").addEventListener("click", showNickScreen);

document.getElementById("startStreakBtn").addEventListener("click", function () {
    const nick = document.getElementById("nickInput").value.trim();
    if (!nick) { alert("Enter a nick!"); return; }
    startStreak(nick);
});

document.getElementById("backFromNickBtn").addEventListener("click", showMenu);
document.getElementById("backBtn").addEventListener("click", showMenu);

window.addEventListener("load", showMenu);
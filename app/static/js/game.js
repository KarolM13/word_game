let currentGameId = null;
let wordLength = 0;
let currentCategory = "";

window.addEventListener('load', function() {
    startNewGame();
});
function updateInfo(remaining) {
    document.getElementById("info").textContent =
        `Category: ${currentCategory} | Letters: ${wordLength} | Attempts remaining: ${remaining}`;
}
function startNewGame() {
    document.getElementById("board").innerHTML = "";
    document.getElementById("guess").value = "";

    fetch("/api/new_game", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        currentGameId = data.game_id;
        wordLength = data.word_length;
        currentCategory = data.category

        const input = document.getElementById("guess");
        input.maxLength = wordLength;
        input.minLength = wordLength;
        input.placeholder = "─".repeat(wordLength);
        updateInfo(data.max_attempts)

    })
    .catch(error => console.error('Error starting game:', error));
}

document.getElementById("guessBtn").addEventListener("click", function() {
    const guessValue = document.getElementById("guess").value.trim();

    if (!currentGameId) {
        startNewGame();
        return;
    }

    if (!guessValue) {
        alert("Enter a word!");
        return;
    }

    if (guessValue.length !== wordLength) {
        alert(`Word must be exactly ${wordLength} letters!`);
        return;
    }

    fetch("/api/guess", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ guess: guessValue, game_id: currentGameId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        const board = document.getElementById("board");
        const row = document.createElement("div");
        row.classList.add("guess-row");

        data.result.forEach((color, index) => {
            const letter = document.createElement("span");
            letter.textContent = guessValue[index];
            letter.classList.add(color);
            row.appendChild(letter);
        });

        board.appendChild(row);

        if (data.is_won) {
            const msg = document.createElement("p");
            msg.textContent = "Congratulations! You won! 🎉";
            msg.classList.add("message", "win");
            board.appendChild(msg);
            currentGameId = null;
        } else if (data.is_over) {
            const msg = document.createElement("p");
            msg.textContent = `Game over! The word was: "${data.answer.toUpperCase()}"`;
            msg.classList.add("message", "lose");
            board.appendChild(msg);
            currentGameId = null;
        } else {
            updateInfo(data.remaining)
        }

        document.getElementById("guess").value = "";
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById("newGameBtn").addEventListener("click", function() {
    startNewGame();
});
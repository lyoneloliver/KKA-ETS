document.addEventListener("DOMContentLoaded", () => {

    const allRows = document.querySelectorAll(".row");
    const sendButton = document.getElementById("send-feedback-btn");
    const resetButton = document.getElementById("reset-btn");
    const messageLog = document.getElementById("message-log");
    const langCheckbox = document.getElementById("lang-checkbox");

    const ui = {
        title: document.getElementById('header-title'),
        subtitle: document.getElementById('header-subtitle'),
        sendBtn: document.getElementById('send-feedback-btn'),
        resetBtn: document.getElementById('reset-btn')
    };

    const translations = {
        en: {
            title: "Wordle Solver",
            subtitle: "Let Python guess, you provide the color feedback.",
            send_btn: "Send Feedback",
            reset_btn: "Reset",
            loading_dict: "Loading English dictionary...",
            feedback_prompt: "Click the tiles to give color feedback.",
            thinking: "Solver is thinking...",
            success: "Success! The word was found. 🎉",
            fail_no_match: "Solver gave up. No matching word in the dictionary.",
            fail_no_tries: "Failed to find the word in 6 tries.",
            fail_connection: "Failed to connect to the server.", // Pesan digeneralisasi
            fail_no_guess: "Failed to load guess."
        },
        id: {
            title: "Wordle Solver",
            subtitle: "Biar Python menebak, Anda yang memberi umpan balik warna.",
            send_btn: "Kirim Umpan Balik",
            reset_btn: "Mulai Ulang",
            loading_dict: "Memuat kamus Indonesia...",
            feedback_prompt: "Klik kotak untuk memberi umpan balik warna.",
            thinking: "Solver sedang berpikir...",
            success: "Berhasil! Kata ditemukan. 🎉",
            fail_no_match: "Solver menyerah. Tidak ada kata yang cocok di kamus.",
            fail_no_tries: "Gagal menemukan kata dalam 6 percobaan.",
            fail_connection: "Gagal terhubung ke server.", // Pesan digeneralisasi
            fail_no_guess: "Gagal memuat tebakan."
        }
    };

    let currentRowIndex = 0;
    let gameActive = true;
    let knownGreens = {};
    let currentLang = 'en'; 

    function updateLanguage(lang) {
        const t = translations[lang];
        ui.title.textContent = t.title;
        ui.subtitle.textContent = t.subtitle;
        ui.sendBtn.textContent = t.send_btn;
        ui.resetBtn.textContent = t.reset_btn;
    }

    function getMessage(key, lang = currentLang, extraInfo = "") {
        if (key && translations[lang][key]) {
            return translations[lang][key];
        }
        return extraInfo || key;
    }

    function createEmptyGrid() {
        allRows.forEach(row => {
            row.innerHTML = '';
            for (let i = 0; i < 5; i++) {
                const tile = document.createElement("div");
                tile.classList.add("tile");
                row.appendChild(tile);
            }
        });
    }

    function changeColor(tile, rIndex, direction = 1) {
        if (rIndex !== currentRowIndex || !gameActive || !tile.textContent || tile.classList.contains("locked")) {
            return;
        }

        const colors = ["gray", "yellow", "green"];
        let currentColorIndex = colors.findIndex(c => tile.classList.contains(c));

        colors.forEach(c => tile.classList.remove(c));

        if (direction === 1) {
            currentColorIndex = (currentColorIndex + 1) % colors.length;
        } else {
            currentColorIndex = (currentColorIndex - 1 + colors.length) % colors.length;
        }

        tile.classList.add(colors[currentColorIndex]);
    }

    function displayGuess(guess, rIndex) {
        const row = allRows[rIndex];
        if (!row) return;

        row.innerHTML = '';

        guess.split("").forEach((letter, i) => {
            const tile = document.createElement("div");
            tile.classList.add("tile");
            tile.dataset.index = i;
            tile.textContent = letter.toUpperCase();

            if (knownGreens[i] === letter.toLowerCase()) {
                tile.classList.add("green", "locked");
            } else {
                tile.classList.add("gray");
            }

            tile.addEventListener("click", (e) => {
                e.preventDefault();
                changeColor(tile, rIndex, 1);
            });

            tile.addEventListener("contextmenu", (e) => {
                e.preventDefault();
                changeColor(tile, rIndex, -1);
            });

            row.appendChild(tile);
        });

        row.classList.add("active");
        sendButton.disabled = false;
    }

    async function sendFeedback() {
        if (!gameActive) return;

        const activeRow = allRows[currentRowIndex];
        const tiles = activeRow.querySelectorAll(".tile");
        let feedback = "";

        tiles.forEach((tile) => {
            const letter = tile.textContent.toLowerCase();
            const index = tile.dataset.index;
            if (tile.classList.contains("green")) {
                feedback += "g";
                knownGreens[index] = letter;
            } else if (tile.classList.contains("yellow")) {
                feedback += "y";
            } else {
                feedback += "b";
            }
        });

        if (feedback === "ggggg") {
            messageLog.textContent = getMessage('success');
            gameActive = false;
            sendButton.disabled = true;
            return;
        }

        try {
            messageLog.textContent = getMessage('thinking');
            sendButton.disabled = true;


            const res = await fetch("/api/feedback", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ feedback })
            });
            const data = await res.json();

            activeRow.classList.remove("active");
            currentRowIndex++;

            if (data.guess && currentRowIndex < 6) {
                displayGuess(data.guess, currentRowIndex);
                messageLog.textContent = getMessage('feedback_prompt', currentLang, data.message);
            } else {
                gameActive = false;
                sendButton.disabled = true;
                messageLog.textContent = getMessage(data.message || 'fail_no_tries');
            }
        } catch (error) {
            messageLog.textContent = getMessage('fail_connection');
        }
    }

    function resetGame() {
        currentRowIndex = 0;
        gameActive = true;
        knownGreens = {};
        sendButton.disabled = true;

        updateLanguage(currentLang);
        startGame(currentLang);
    }

    async function startGame(lang) {
        createEmptyGrid();
        messageLog.textContent = getMessage('loading_dict', lang);

        try {
            const res = await fetch(`/api/start_game?lang=${lang}`);
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

            const data = await res.json();
            if (data.guess) {
                displayGuess(data.guess, 0);
                messageLog.textContent = getMessage('feedback_prompt');
            } else {
                messageLog.textContent = getMessage('fail_no_guess');
            }
        } catch (error) {
            messageLog.textContent = getMessage('fail_connection');
        }
    }

    sendButton.addEventListener("click", sendFeedback);
    resetButton.addEventListener("click", resetGame);

    langCheckbox.addEventListener('change', () => {
        currentLang = langCheckbox.checked ? 'id' : 'en';
        resetGame();
    });

    resetGame();
});
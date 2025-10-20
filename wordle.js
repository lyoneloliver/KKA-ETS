// wordle.js

document.addEventListener("DOMContentLoaded", () => {
    
    const allRows = document.querySelectorAll(".row");
    const sendButton = document.getElementById("send-feedback-btn");
    const resetButton = document.getElementById("reset-btn");
    const messageLog = document.getElementById("message-log");
    
    // Variabel bahasa dan checkbox telah dihapus
    
    let currentRowIndex = 0;
    let gameActive = true;
    let knownGreens = {}; // Memori untuk tile hijau

    // 1. Buat petak permainan 6x5
    allRows.forEach((row, rIndex) => {
        for (let i = 0; i < 5; i++) {
            const tile = document.createElement("div");
            tile.classList.add("tile");
            tile.dataset.index = i; 
            tile.addEventListener("click", () => toggleColor(tile, rIndex));
            row.appendChild(tile);
        }
    });

    // 2. Fungsi untuk mengubah warna tile
    function toggleColor(tile, rIndex) {
        if (rIndex !== currentRowIndex || !gameActive || !tile.textContent || tile.classList.contains("locked")) {
            return;
        }
        if (tile.classList.contains("yellow")) {
            tile.classList.replace("yellow", "green");
        } else if (tile.classList.contains("green")) {
            tile.classList.replace("green", "gray");
        } else {
            tile.classList.remove("gray");
            tile.classList.add("yellow");
        }
    }

    // 3. Fungsi untuk menampilkan tebakan (termasuk mengunci tile hijau)
    function displayGuess(guess, rIndex) {
        const row = allRows[rIndex];
        if (!row) return;
        const tiles = row.querySelectorAll(".tile");
        guess.split("").forEach((letter, i) => {
            tiles[i].textContent = letter.toUpperCase();
            if (knownGreens[i] === letter.toLowerCase()) {
                tiles[i].classList.add("green", "locked");
            } else {
                tiles[i].classList.add("gray");
            }
        });
        row.classList.add("active");
        sendButton.disabled = false;
    }
    
    // 4. Fungsi untuk mengirim feedback ke server
    async function sendFeedback() {
        if (!gameActive) return;

        const activeRow = allRows[currentRowIndex];
        const tiles = activeRow.querySelectorAll(".tile");
        let feedback = "";

        // Update memori 'knownGreens'
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
            messageLog.textContent = "Berhasil! Kata ditemukan. 🎉";
            gameActive = false; sendButton.disabled = true; return;
        }

        try {
            messageLog.textContent = "Solver sedang berpikir...";
            sendButton.disabled = true;
            
            const res = await fetch("http://127.0.0.1:5000/feedback", {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ feedback: feedback })
            });
            const data = await res.json();

            activeRow.classList.remove("active");
            currentRowIndex++;

            if (data.guess && currentRowIndex < 6) {
                displayGuess(data.guess, currentRowIndex);
                messageLog.textContent = data.message || "Masukkan feedback untuk tebakan baru.";
            } else {
                gameActive = false; sendButton.disabled = true;
                messageLog.textContent = data.message || "Gagal menemukan kata dalam 6 percobaan.";
            }
        } catch (error) {
            messageLog.textContent = "Koneksi ke server Python gagal. Pastikan server berjalan.";
        }
    }

    // 5. Fungsi untuk mereset permainan
    function resetGame() {
        // Cukup reload halaman. Ini akan otomatis memanggil startGame()
        // dan server akan mereset statenya.
        location.reload();
    }

    // 6. Fungsi untuk memulai permainan
    async function startGame() {
        knownGreens = {}; // Reset memori hijau
        try {
            messageLog.textContent = "Memuat kamus...";
            
            // Panggil /start_game (tanpa parameter bahasa)
            const res = await fetch("http://127.0.0.1:5000/start_game");
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
            
            const data = await res.json();
            if (data.guess) {
                displayGuess(data.guess, 0);
                messageLog.textContent = "Klik kotak untuk memberi feedback warna.";
            } else {
                messageLog.textContent = "Gagal memuat tebakan.";
            }
        } catch (error) {
            messageLog.textContent = "Gagal terhubung ke server Python. Pastikan server berjalan.";
        }
    }
    
    // 7. Event listener untuk tombol
    sendButton.addEventListener("click", sendFeedback);
    resetButton.addEventListener("click", resetGame);
    
    // Mulai permainan saat halaman dimuat
    startGame();
});
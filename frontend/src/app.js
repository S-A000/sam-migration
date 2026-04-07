// --- SaaS Frontend Logic ---

const API_BASE_URL = "http://localhost:8000/api";
const WS_BASE_URL = "ws://localhost:8000/ws";

// 1. Connection Test Logic
async function testConnection(credentials) {
    console.log("🔍 Validating Source...");
    const response = await fetch(`${API_BASE_URL}/connections/test`, {
        method: 'POST',
        body: JSON.stringify(credentials),
        headers: { 'Content-Type': 'application/json' }
    });
    return await response.json();
}

// 2. WebSocket Stream (Live Logs & Progress)
function startLiveMonitor(jobId) {
    const socket = new WebSocket(`${WS_BASE_URL}/migration/${jobId}`);

    socket.onmessage = (event) => {
        const message = JSON.parse(event.data);

        if (message.type === "LOG") {
            updateTerminal(message.data); // Aapke Terminal UI mein add karega
        }
        if (message.type === "PROGRESS") {
            updateProgressBar(message.data); // Progress bar ko move karega
        }
    };
}

// UI Helpers (Inko aapke HTML IDs ke sath connect karenge)
function updateTerminal(logText) {
    const terminal = document.getElementById('terminal-content');
    if (terminal) terminal.innerHTML += `<div>${logText}</div>`;
}

function updateProgressBar(percent) {
    const bar = document.getElementById('main-progress-bar');
    if (bar) bar.style.width = `${percent}%`;
}

// --- SaaS Connection Manager Logic ---

document.addEventListener('DOMContentLoaded', () => {
    const testBtn = document.querySelector('button:contains("Test Connection")'); // Target the button

    if (testBtn) {
        testBtn.addEventListener('click', async () => {
            // UI Update: Button ko loading state mein le jayen
            testBtn.innerHTML = '<span class="animate-spin material-symbols-outlined">sync</span> Testing...';

            // 1. Inputs se data uthayein
            const sourceIP = document.querySelector('input[placeholder="e.g. 10.0.0.1"]').value;
            const dbName = document.querySelector('input[placeholder="Enter DB name"]').value;

            try {
                // 2. Backend API Call
                const response = await fetch('http://localhost:8000/api/connections/test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ source_ip: sourceIP, db_name: dbName })
                });

                const result = await response.json();

                if (response.ok) {
                    // Success UI: Notification show karein
                    showToast("✅ Source Validated Successfully!", "success");
                } else {
                    showToast("❌ Connection Failed: Check Credentials", "error");
                }
            } catch (err) {
                showToast("⚠️ Backend Server Offline!", "error");
            } finally {
                testBtn.innerHTML = '<span class="material-symbols-outlined">network_check</span> Test Connection';
            }
        });
    }
});

// Toast Notification Helper
function showToast(message, type) {
    const toast = document.querySelector('.glass-panel'); // Target your floating toast
    toast.style.display = 'flex';
    toast.querySelector('p.text-xs').innerText = message;
}
// monitor.js
export const initMonitor = (jobId) => {
    const socket = new WebSocket(`ws://localhost:8000/ws/migration/${jobId}`);
    const progressBar = document.querySelector('.progress-glow'); // Aapki Tailwind class
    const percentageText = document.querySelector('.text-6xl');

    socket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.type === "PROGRESS") {
            const percent = message.data;
            progressBar.style.width = `${percent}%`;
            percentageText.innerHTML = `${percent}<span class="text-2xl text-primary-container">%</span>`;
        }
    };
};
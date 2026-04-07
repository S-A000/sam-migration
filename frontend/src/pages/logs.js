// logs.js
export const updateTerminal = (logMessage, type = "INFO") => {
    const terminal = document.querySelector('.terminal-scroll');
    const time = new Date().toLocaleTimeString([], { hour12: false });

    const logLine = document.createElement('div');
    logLine.className = 'text-slate-400 mb-2';

    // Type ke hisab se color change karein
    const typeColor = type === "ERR" ? "text-rose-500" : "text-blue-400";

    logLine.innerHTML = `
        <span class="text-emerald-400">[${time}]</span> 
        <span class="${typeColor} font-bold">${type}</span> ${logMessage}
    `;

    terminal.appendChild(logLine);
    terminal.scrollTop = terminal.scrollHeight; // Auto scroll to bottom
};
// connection_manager.js
export const initConnectionManager = () => {
    const testBtn = document.getElementById('test-connection-btn');

    testBtn?.addEventListener('click', async () => {
        // Inputs se data uthayein
        const sourceData = {
            ip: document.querySelector('[placeholder="e.g. 10.0.0.1"]').value,
            db: document.querySelector('[placeholder="Enter DB name"]').value,
            user: document.querySelector('[placeholder="Service account name"]').value,
            pass: document.querySelector('[type="password"]').value
        };

        console.log("🔄 Testing Handshake...");

        try {
            const response = await fetch('http://localhost:8000/api/connections/test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(sourceData)
            });
            const result = await response.json();
            alert(result.message); // Real SaaS mein hum toast notification use karenge
        } catch (err) {
            console.error("❌ API Error:", err);
        }
    });
};
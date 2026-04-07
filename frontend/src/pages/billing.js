// billing.js
export const loadBillingStats = async () => {
    const response = await fetch('http://localhost:8000/api/billing/summary');
    const stats = await response.json();

    // UI elements update karein
    document.querySelector('.text-7xl').innerText = `${stats.total_tb} TB`;
    document.querySelector('.text-primary').innerText = `${stats.projected_cost}`;
};
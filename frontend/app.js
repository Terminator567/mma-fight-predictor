const API_BASE_URL = 'http://127.0.0.1:8000/api';
let allFighters = [];

document.addEventListener('DOMContentLoaded', async () => {
    await loadAllFighters();
    setupEventListeners();
});

async function loadAllFighters() {
    try {
        const response = await fetch(`${API_BASE_URL}/fighters`);
        if (response.ok) {
            allFighters = await response.json();
        }
    } catch (error) {
        console.log('Could not load fighters list, autocomplete will be limited');
    }
}

function setupEventListeners() {
    const fighter1Input = document.getElementById('fighter1');
    const fighter2Input = document.getElementById('fighter2');
    const predictBtn = document.getElementById('predictBtn');

    fighter1Input.addEventListener('input', (e) => handleInput(e, 'suggestions1'));
    fighter2Input.addEventListener('input', (e) => handleInput(e, 'suggestions2'));

    fighter1Input.addEventListener('blur', () => {
        setTimeout(() => document.getElementById('suggestions1').classList.remove('active'), 200);
    });

    fighter2Input.addEventListener('blur', () => {
        setTimeout(() => document.getElementById('suggestions2').classList.remove('active'), 200);
    });

    predictBtn.addEventListener('click', makePrediction);

    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('suggestion-item')) {
            const fighter = e.target.textContent;
            if (e.target.closest('#suggestions1')) {
                document.getElementById('fighter1').value = fighter;
                document.getElementById('suggestions1').classList.remove('active');
            } else if (e.target.closest('#suggestions2')) {
                document.getElementById('fighter2').value = fighter;
                document.getElementById('suggestions2').classList.remove('active');
            }
        }
    });
}

function handleInput(event, suggestionsId) {
    const input = event.target.value.trim().toLowerCase();
    const suggestionsContainer = document.getElementById(suggestionsId);

    if (input.length < 2) {
        suggestionsContainer.classList.remove('active');
        return;
    }

    const filtered = allFighters
        .filter(fighter => fighter.toLowerCase().includes(input))
        .slice(0, 8);

    if (filtered.length === 0) {
        suggestionsContainer.classList.remove('active');
        return;
    }

    suggestionsContainer.innerHTML = filtered
        .map(fighter => `<li class="suggestion-item">${fighter}</li>`)
        .join('');
    suggestionsContainer.classList.add('active');
}

async function makePrediction() {
    const fighter1 = document.getElementById('fighter1').value.trim();
    const fighter2 = document.getElementById('fighter2').value.trim();
    const predictBtn = document.getElementById('predictBtn');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');

    if (!fighter1 || !fighter2) {
        showError('Please enter both fighter names');
        return;
    }

    if (fighter1.toLowerCase() === fighter2.toLowerCase()) {
        showError('Please select two different fighters');
        return;
    }

    predictBtn.disabled = true;
    loadingDiv.classList.remove('hidden');
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');

    try {
        const response = await fetch(
            `${API_BASE_URL}/predict?fighter1=${encodeURIComponent(fighter1)}&fighter2=${encodeURIComponent(fighter2)}`,
            { method: 'POST' }
        );

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayResult(data, fighter1, fighter2);
        loadingDiv.classList.add('hidden');
        resultDiv.classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        showError(`Failed to make prediction: ${error.message}`);
        loadingDiv.classList.add('hidden');
    } finally {
        predictBtn.disabled = false;
    }
}

function displayResult(data, fighter1, fighter2) {
    document.getElementById('resultFighter1').textContent = fighter1;
    document.getElementById('resultFighter2').textContent = fighter2;

    document.getElementById('weight1').textContent = data.fighter1_info.weight_class || 'N/A';
    document.getElementById('kd1').textContent = data.fighter1_info.total_kd || 0;
    document.getElementById('str1').textContent = data.fighter1_info.total_str || 0;
    document.getElementById('td1').textContent = data.fighter1_info.total_td || 0;
    document.getElementById('sub1').textContent = data.fighter1_info.total_sub || 0;

    document.getElementById('weight2').textContent = data.fighter2_info.weight_class || 'N/A';
    document.getElementById('kd2').textContent = data.fighter2_info.total_kd || 0;
    document.getElementById('str2').textContent = data.fighter2_info.total_str || 0;
    document.getElementById('td2').textContent = data.fighter2_info.total_td || 0;
    document.getElementById('sub2').textContent = data.fighter2_info.total_sub || 0;

    const winner = data.prediction.winner;
    const confidence = data.prediction.confidence;
    
    document.getElementById('resultFighter1').style.color = winner === 1 ? '#ffa500' : '#888';
    document.getElementById('resultFighter2').style.color = winner === 2 ? '#ffa500' : '#888';

    const winnerName = winner === 1 ? fighter1 : fighter2;
    document.getElementById('winnerBadge').textContent = '🏆';
    document.getElementById('winnerText').textContent = `${winnerName} will likely win!`;
    document.getElementById('confidence').textContent = `Confidence: ${(confidence * 100).toFixed(1)}%`;
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function closeResult() {
    document.getElementById('result').classList.add('hidden');
    document.getElementById('fighter1').value = '';
    document.getElementById('fighter2').value = '';
    document.getElementById('fighter1').focus();
}
/**
 * ai_recommend_detail.js
 * Renders a single recipe on the detail page. Tries sessionStorage first
 * (instant, set by ai_recommend.js when the card was clicked); falls back
 * to GET /api/recipe/<id>/ for direct URL visits or expired sessions.
 */

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
}
function renderDetail(recipe) {
    document.getElementById('d-name').textContent = recipe.name || 'Untitled Recipe';
    document.getElementById('d-minutes').textContent = `${recipe.minutes ?? '?'} mins`;
    document.getElementById('d-score').textContent = recipe.score !== null && recipe.score !== undefined
        ? `${Math.round(recipe.score * 100)}%`
        : 'N/A';

    const ingredientsEl = document.getElementById('d-ingredients');
    ingredientsEl.innerHTML = (recipe.ingredients || [])
        .map(i => `<li class="list-group-item"><i class="fas fa-check-circle text-success"></i> ${escapeHtml(i)}</li>`)
        .join('');

    const stepsEl = document.getElementById('d-steps');
    stepsEl.innerHTML = (recipe.steps || [])
        .map(s => `<li class="list-group-item">${escapeHtml(s)}</li>`)
        .join('');

    document.getElementById('detail-loading').classList.add('d-none');
    document.getElementById('detail-content').classList.remove('d-none');
}

function showError(message) {
    document.getElementById('detail-loading').classList.add('d-none');
    const errorEl = document.getElementById('detail-error');
    errorEl.textContent = message;
    errorEl.classList.remove('d-none');
}

async function loadRecipe() {
    const cached = sessionStorage.getItem(`ai_recipe_${RECIPE_ID}`);
    if (cached) {
        renderDetail(JSON.parse(cached));
        return;
    }

    try {
        const response = await fetch(`/api/recipe/${RECIPE_ID}/`);
        const data = await response.json();

        if (!response.ok) {
            showError(data.error || 'Recipe not found.');
            return;
        }
        renderDetail(data);
    } catch (err) {
        showError('Network error loading this recipe.');
        console.error('Recipe detail fetch failed:', err);
    }
}

document.addEventListener('DOMContentLoaded', loadRecipe);
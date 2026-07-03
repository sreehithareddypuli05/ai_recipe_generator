/**
 * ai_recommend.js
 * Handles the AI ingredient-search page: calls /api/recommend/, renders
 * recipe cards, and stores the clicked recipe in sessionStorage so the
 * detail page can render instantly without a second network round trip
 * (falls back to /api/recipe/<id>/ if sessionStorage is empty, e.g. on
 * direct URL visits).
 */

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
}

const CSRF_TOKEN = getCookie('csrftoken');

async function searchRecipes(ingredients) {
    const resultsEl = document.getElementById('ai-results');
    const errorEl = document.getElementById('ai-error');
    const loadingEl = document.getElementById('ai-loading');

    errorEl.classList.add('d-none');
    resultsEl.innerHTML = '';
    loadingEl.classList.remove('d-none');

    try {
        const response = await fetch('/api/recommend/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN,
            },
            body: JSON.stringify({ ingredients }),
        });

        const data = await response.json();
        loadingEl.classList.add('d-none');

        if (!response.ok) {
            const msg = data.error || 'Something went wrong. Please try again.';
            errorEl.textContent = msg;
            errorEl.classList.remove('d-none');
            return;
        }

        if (data.length === 0) {
            resultsEl.innerHTML = '<div class="col-12"><div class="alert alert-warning">No matching recipes found. Try different ingredients.</div></div>';
            return;
        }

        resultsEl.innerHTML = data.map(renderCard).join('');
    } catch (err) {
        loadingEl.classList.add('d-none');
        errorEl.textContent = 'Network error — please check your connection and try again.';
        errorEl.classList.remove('d-none');
        console.error('Recommend request failed:', err);
    }
}

function renderCard(recipe) {
    const ingredientsPreview = (recipe.ingredients || []).slice(0, 5).join(', ');
    const scorePct = recipe.score !== null ? Math.round(recipe.score * 100) : null;

    return `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card recipe-card h-100">
                <div class="card-body d-flex flex-column">
                    <div class="mb-2" style="height:120px; background:#f0f0f0; border-radius:10px; display:flex; align-items:center; justify-content:center;">
                        <i class="fas fa-utensils fa-3x text-muted"></i>
                    </div>
                    <h5 class="card-title">${escapeHtml(recipe.name || 'Untitled Recipe')}</h5>
                    <div class="mb-2">
                        <span class="badge bg-info"><i class="fas fa-clock"></i> ${recipe.minutes ?? '?'} min</span>
                        ${scorePct !== null ? `<span class="badge bg-secondary">${scorePct}% match</span>` : ''}
                    </div>
                    <p class="text-muted small flex-grow-1">${escapeHtml(ingredientsPreview)}${recipe.ingredients && recipe.ingredients.length > 5 ? '...' : ''}</p>
                    <button class="btn btn-primary btn-sm mt-2" onclick='viewRecipe(${JSON.stringify(recipe)})'>
                        <i class="fas fa-eye"></i> View Recipe
                    </button>
                </div>
            </div>
        </div>
    `;
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
}

function viewRecipe(recipe) {
    sessionStorage.setItem(`ai_recipe_${recipe.id}`, JSON.stringify(recipe));
    window.location.href = `/ai-recommend/${recipe.id}/`;
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('ai-search-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const raw = document.getElementById('ingredients-input').value;
        const ingredients = raw.split(',').map(i => i.trim()).filter(Boolean);

        if (ingredients.length === 0) {
            const errorEl = document.getElementById('ai-error');
            errorEl.textContent = 'Please enter at least one ingredient.';
            errorEl.classList.remove('d-none');
            return;
        }
        searchRecipes(ingredients);
    });
});
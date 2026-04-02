/* Ad Report Application */

const API_BASE = "https://emissions-stay-jacob-engaged.trycloudflare.com/api/ads";


// DOM Elements
const addAdForm = document.getElementById('addAdForm');
const editAdForm = document.getElementById('editAdForm');
const adTableBody = document.getElementById('adTableBody');
const noEntriesMessage = document.getElementById('noEntriesMessage');
const editModal = document.getElementById('editModal');
const closeModalBtn = document.querySelector('.close');
const cancelEditBtn = document.getElementById('cancelEdit');

// Summary Elements
const totalImpressionsEl = document.getElementById('totalImpressions');
const totalClicksEl = document.getElementById('totalClicks');
const totalCostEl = document.getElementById('totalCost');
const ctrEl = document.getElementById('ctr');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadAds();
    addAdForm.addEventListener('submit', handleAddAd);
    editAdForm.addEventListener('submit', handleEditAd);
    closeModalBtn.addEventListener('click', closeEditModal);
    cancelEditBtn.addEventListener('click', closeEditModal);
    window.addEventListener('click', (e) => {
        if (e.target === editModal) closeEditModal();
    });
});

// Load all ads from API
async function loadAds() {
    try {
        const response = await fetch(API_BASE);
        if (!response.ok) throw new Error('Failed to load ads');
        
        const ads = await response.json();
        renderAds(ads);
        updateSummary(ads);
    } catch (error) {
        console.error('Error loading ads:', error);
    }
}

// Render ads in table
function renderAds(ads) {
    adTableBody.innerHTML = '';
    
    if (ads.length === 0) {
        adTableBody.innerHTML = '<tr id="noEntriesMessage"><td colspan="7" class="no-entries">No ad entries yet. Add your first entry above!</td></tr>';
        return;
    }

    ads.forEach(ad => {
        const ctr = ad.impressions > 0 ? ((ad.clicks / ad.impressions) * 100).toFixed(2) : 0;
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${ad.campaign}</td>
            <td>${ad.impressions.toLocaleString()}</td>
            <td>${ad.clicks.toLocaleString()}</td>
            <td>${ctr}%</td>
            <td>$${ad.cost.toFixed(2)}</td>
            <td>${ad.conversions || 0}</td>
            <td>
                <button class="btn btn-primary btn-sm" onclick="editAd(${ad.id})">Edit</button>
                <button class="btn btn-secondary btn-sm" onclick="deleteAd(${ad.id})">Delete</button>
            </td>
        `;
        adTableBody.appendChild(row);
    });
}

// Update summary statistics
function updateSummary(ads) {
    const totalImpressions = ads.reduce((sum, ad) => sum + ad.impressions, 0);
    const totalClicks = ads.reduce((sum, ad) => sum + ad.clicks, 0);
    const totalCost = ads.reduce((sum, ad) => sum + ad.cost, 0);
    const ctr = totalImpressions > 0 ? ((totalClicks / totalImpressions) * 100).toFixed(2) : 0;

    totalImpressionsEl.textContent = totalImpressions.toLocaleString();
    totalClicksEl.textContent = totalClicks.toLocaleString();
    totalCostEl.textContent = `$${totalCost.toFixed(2)}`;
    ctrEl.textContent = `${ctr}%`;
}

// Handle add ad form submission
async function handleAddAd(e) {
    e.preventDefault();
    
    const formData = new FormData(addAdForm);
    const adData = {
        campaign: formData.get('campaign'),
        impressions: parseInt(formData.get('impressions')),
        clicks: parseInt(formData.get('clicks')),
        cost: parseFloat(formData.get('cost')),
        conversions: parseInt(formData.get('conversions')) || 0,
        notes: formData.get('notes') || ''
    };

    try {
        const response = await fetch(API_BASE, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(adData)
        });

        if (!response.ok) throw new Error('Failed to add ad');
        
        addAdForm.reset();
        loadAds();
    } catch (error) {
        console.error('Error adding ad:', error);
        alert('Failed to add ad entry. Please try again.');
    }
}

// Handle edit ad form submission
async function handleEditAd(e) {
    e.preventDefault();
    
    const formData = new FormData(editAdForm);
    const adData = {
        campaign: formData.get('campaign'),
        impressions: parseInt(formData.get('impressions')),
        clicks: parseInt(formData.get('clicks')),
        cost: parseFloat(formData.get('cost')),
        conversions: parseInt(formData.get('conversions')) || 0,
        notes: formData.get('notes') || ''
    };

    const adId = formData.get('id');

    try {
        const response = await fetch(`${API_BASE}/${adId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(adData)
        });

        if (!response.ok) throw new Error('Failed to update ad');
        
        closeEditModal();
        loadAds();
    } catch (error) {
        console.error('Error updating ad:', error);
        alert('Failed to update ad entry. Please try again.');
    }
}

// Edit ad
async function editAd(id) {
    try {
        const response = await fetch(`${API_BASE}/${id}`);
        if (!response.ok) throw new Error('Failed to load ad');
        
        const ad = await response.json();
        
        document.getElementById('editId').value = ad.id;
        document.getElementById('editCampaign').value = ad.campaign;
        document.getElementById('editImpressions').value = ad.impressions;
        document.getElementById('editClicks').value = ad.clicks;
        document.getElementById('editCost').value = ad.cost;
        document.getElementById('editConversions').value = ad.conversions || 0;
        document.getElementById('editNotes').value = ad.notes || '';
        
        editModal.style.display = 'block';
    } catch (error) {
        console.error('Error loading ad for edit:', error);
    }
}

// Delete ad
async function deleteAd(id) {
    if (!confirm('Are you sure you want to delete this ad entry?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete ad');
        
        loadAds();
    } catch (error) {
        console.error('Error deleting ad:', error);
        alert('Failed to delete ad entry. Please try again.');
    }
}

// Close edit modal
function closeEditModal() {
    editModal.style.display = 'none';
    editAdForm.reset();
}
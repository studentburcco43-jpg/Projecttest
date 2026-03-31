/* Profit Summary Application */

const API_BASE = "https://ing-speakers-invoice-vbulletin.trycloudflare.com/api/profits";


// DOM Elements
const addProfitForm = document.getElementById('addProfitForm');
const editProfitForm = document.getElementById('editProfitForm');
const profitTableBody = document.getElementById('profitTableBody');
const noEntriesMessage = document.getElementById('noEntriesMessage');
const editModal = document.getElementById('editModal');
const closeModalBtn = document.querySelector('.close');
const cancelEditBtn = document.getElementById('cancelEdit');

// Summary Elements
const totalRevenueEl = document.getElementById('totalRevenue');
const totalExpensesEl = document.getElementById('totalExpenses');
const totalProfitEl = document.getElementById('totalProfit');
const profitMarginEl = document.getElementById('profitMargin');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadProfits();
    addProfitForm.addEventListener('submit', handleAddProfit);
    editProfitForm.addEventListener('submit', handleEditProfit);
    closeModalBtn.addEventListener('click', closeEditModal);
    cancelEditBtn.addEventListener('click', closeEditModal);
    window.addEventListener('click', (e) => {
        if (e.target === editModal) closeEditModal();
    });
});

// Load all profits from API
async function loadProfits() {
    try {
        const response = await fetch(API_BASE);
        if (!response.ok) throw new Error('Failed to load profits');
        
        const profits = await response.json();
        renderProfits(profits);
        updateSummary(profits);
    } catch (error) {
        console.error('Error loading profits:', error);
    }
}

// Render profits in table
function renderProfits(profits) {
    profitTableBody.innerHTML = '';
    
    if (profits.length === 0) {
        noEntriesMessage.style.display = 'block';
    } else {
        noEntriesMessage.style.display = 'none';
        profits.forEach(profit => {
            const row = createTableRow(profit);
            profitTableBody.appendChild(row);
        });
    }
}

// Create table row for a profit entry
function createTableRow(profit) {
    const row = document.createElement('tr');
    const profitAmount = profit.revenue - profit.expenses;
    const margin = profit.revenue > 0 ? ((profitAmount / profit.revenue) * 100).toFixed(2) : 0;
    
    const profitClass = profitAmount >= 0 ? 'profit-positive' : 'profit-negative';
    const profitSign = profitAmount >= 0 ? '+' : '';
    
    row.innerHTML = `
        <td>${escapeHtml(profit.category)}</td>
        <td class="profit-value">$${profit.revenue.toFixed(2)}</td>
        <td class="profit-value">$${profit.expenses.toFixed(2)}</td>
        <td class="${profitClass}">${profitSign}$${profitAmount.toFixed(2)}</td>
        <td>${margin}%</td>
        <td>${escapeHtml(profit.notes || '')}</td>
        <td>
            <button class="btn btn-edit" onclick="openEditModal(${profit.id})">Edit</button>
            <button class="btn btn-delete" onclick="deleteProfit(${profit.id})">Delete</button>
        </td>
    `;
    return row;
}

// Handle add profit form submission
async function handleAddProfit(e) {
    e.preventDefault();
    
    const profit = {
        category: document.getElementById('category').value,
        revenue: parseFloat(document.getElementById('revenue').value),
        expenses: parseFloat(document.getElementById('expenses').value),
        notes: document.getElementById('notes').value
    };
    
    try {
        const response = await fetch(API_BASE, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profit)
        });
        
        if (!response.ok) throw new Error('Failed to create profit entry');
        
        addProfitForm.reset();
        loadProfits();
    } catch (error) {
        console.error('Error creating profit:', error);
        alert('Failed to create entry. Please try again.');
    }
}

// Open edit modal
async function openEditModal(profitId) {
    try {
        const response = await fetch(`${API_BASE}/${profitId}`);
        if (!response.ok) throw new Error('Failed to fetch profit');
        
        const profit = await response.json();
        
        document.getElementById('editProfitId').value = profit.id;
        document.getElementById('editCategory').value = profit.category;
        document.getElementById('editRevenue').value = profit.revenue;
        document.getElementById('editExpenses').value = profit.expenses;
        document.getElementById('editNotes').value = profit.notes || '';
        
        editModal.style.display = 'block';
    } catch (error) {
        console.error('Error loading profit for edit:', error);
        alert('Failed to load entry. Please try again.');
    }
}

// Close edit modal
function closeEditModal() {
    editModal.style.display = 'none';
    editProfitForm.reset();
}

// Handle edit profit form submission
async function handleEditProfit(e) {
    e.preventDefault();
    
    const profitId = parseInt(document.getElementById('editProfitId').value);
    const updates = {
        category: document.getElementById('editCategory').value,
        revenue: parseFloat(document.getElementById('editRevenue').value),
        expenses: parseFloat(document.getElementById('editExpenses').value),
        notes: document.getElementById('editNotes').value
    };
    
    try {
        const response = await fetch(`${API_BASE}/${profitId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updates)
        });
        
        if (!response.ok) throw new Error('Failed to update profit entry');
        
        closeEditModal();
        loadProfits();
    } catch (error) {
        console.error('Error updating profit:', error);
        alert('Failed to update entry. Please try again.');
    }
}

// Delete profit entry
async function deleteProfit(profitId) {
    if (!confirm('Are you sure you want to delete this entry?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/${profitId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Failed to delete profit entry');
        
        loadProfits();
    } catch (error) {
        console.error('Error deleting profit:', error);
        alert('Failed to delete entry. Please try again.');
    }
}

// Update summary statistics
function updateSummary(profits) {
    let totalRevenue = 0;
    let totalExpenses = 0;
    
    profits.forEach(profit => {
        totalRevenue += profit.revenue;
        totalExpenses += profit.expenses;
    });
    
    const totalProfit = totalRevenue - totalExpenses;
    const profitMargin = totalRevenue > 0 ? ((totalProfit / totalRevenue) * 100).toFixed(2) : 0;
    
    totalRevenueEl.textContent = `$${totalRevenue.toFixed(2)}`;
    totalExpensesEl.textContent = `$${totalExpenses.toFixed(2)}`;
    totalProfitEl.textContent = `$${totalProfit.toFixed(2)}`;
    profitMarginEl.textContent = `${profitMargin}%`;
    
    if (totalProfit < 0) {
        totalProfitEl.style.color = '#f44336';
    } else {
        totalProfitEl.style.color = '#4CAF50';
    }
}

// Utility: Escape HTML to prevent XSS
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

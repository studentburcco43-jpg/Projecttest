const addModal  = new bootstrap.Modal(document.getElementById('addUserModal'));
const editModal = new bootstrap.Modal(document.getElementById('editUserModal'));

async function loadUsers() {
    const res = await fetch('/api/users');
    if (!res.ok) { return; }
    const users = await res.json();
    const tbody = document.getElementById('usersTableBody');
    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No users found.</td></tr>';
        return;
    }
    tbody.innerHTML = users.map(u => `
        <tr data-id="${u.id}">
            <td>${u.id}</td>
            <td>${u.username}</td>
            <td>${u.FirstName}</td>
            <td>${u.LastName}</td>
            <td>${u.LastLoginDate ? new Date(u.LastLoginDate).toLocaleString() : '—'}</td>
            <td>
                <button class="btn btn-sm btn-outline-success me-1" onclick="openEdit(${u.id}, '${u.username}', '${u.FirstName}', '${u.LastName}')">Edit</button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteUser(${u.id})">Delete</button>
            </td>
        </tr>`).join('');
}

document.getElementById('submitAddUserBtn').addEventListener('click', async () => {
    const form = document.getElementById('addUserForm');
    if (!form.reportValidity()) { return; }
    const body = {
        username: document.getElementById('newUsername').value,
        FirstName: document.getElementById('newFirstName').value,
        LastName: document.getElementById('newLastName').value,
        password: document.getElementById('newPassword').value,
    };
    const res = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });
    if (res.ok) {
        form.reset();
        addModal.hide();
        await loadUsers();
    } else {
        const err = await res.json();
        alert(err.detail ?? 'Failed to create user.');
    }
});

function openEdit(id, username, firstName, lastName) {
    document.getElementById('editUserId').value = id;
    document.getElementById('editUsername').value = username;
    document.getElementById('editFirstName').value = firstName;
    document.getElementById('editLastName').value = lastName;
    document.getElementById('editPassword').value = '';
    editModal.show();
}

document.getElementById('saveUserBtn').addEventListener('click', async () => {
    const id = document.getElementById('editUserId').value;
    const body = {
        username: document.getElementById('editUsername').value || null,
        FirstName: document.getElementById('editFirstName').value || null,
        LastName: document.getElementById('editLastName').value || null,
        password: document.getElementById('editPassword').value || null,
    };
    const res = await fetch(`/api/users/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });
    if (res.ok) {
        editModal.hide();
        await loadUsers();
    } else {
        const err = await res.json();
        alert(err.detail ?? 'Failed to update user.');
    }
});

async function deleteUser(id) {
    if (!confirm('Delete this user?')) { return; }
    const res = await fetch(`/api/users/${id}`, { method: 'DELETE' });
    if (res.ok) { await loadUsers(); }
    else {
        const err = await res.json();
        alert(err.detail ?? 'Failed to delete user.');
    }
}

loadUsers();
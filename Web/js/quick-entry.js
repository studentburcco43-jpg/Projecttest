let allEntries = [];
        let allClients = [];
        let allServices = [];

        document.addEventListener('DOMContentLoaded', async function() {
            await loadClients();
            loadServices();
            setTodayDates();
            await loadRecentEntries();
            document.getElementById('clientForm').addEventListener('submit', handleClientSubmit);
            document.getElementById('serviceForm').addEventListener('submit', handleServiceSubmit);
            document.getElementById('incomeForm').addEventListener('submit', handleIncomeSubmit);
            document.getElementById('expenseForm').addEventListener('submit', handleExpenseSubmit);
        });

        function setTodayDates() {
            const today = new Date().toISOString().split('T')[0];
            document.getElementById('incomeDate').value = today;
            document.getElementById('expenseDate').value = today;
        }

        async function loadClients() {
            try {
                const response = await fetch('/api/clients');
                if (!response.ok) throw new Error('Failed to load clients');
                allClients = await response.json();
                refreshClientOptions();
            } catch (error) {
                console.error('Error loading clients:', error);
            }
        }

        function refreshClientOptions(selectedId = '') {
            ['incomeClient', 'expenseClient'].forEach(selectId => {
                const select = document.getElementById(selectId);
                const current = selectedId || select.value;
                select.innerHTML = '<option value="">Select a client...</option>';
                allClients.forEach(client => {
                    const option = document.createElement('option');
                    option.value = client.id;
                    option.textContent = client.ClientName;
                    select.appendChild(option);
                });
                if (current) {
                    select.value = String(current);
                }
            });
        }

        async function loadServices() {
            try {
                const response = await fetch('/api/services');
                if (!response.ok) throw new Error('Failed to load services');
                allServices = await response.json();

                refreshServiceOptions();
            } catch (error) {
                console.error('Error loading services:', error);
            }
        }

        function refreshServiceOptions(selectedId = '') {
            const select = document.getElementById('incomeService');
            select.innerHTML = '<option value="">Select a service...</option>';

            allServices.forEach(service => {
                const option = document.createElement('option');
                option.value = service.id;
                option.textContent = `${service.ServiceName} ($${service.Cost.toFixed(2)})`;
                select.appendChild(option);
            });

            if (selectedId) {
                select.value = String(selectedId);
            }
        }

        function findClientByName(clientName) {
            return allClients.find(client => client.ClientName.toLowerCase() === clientName.toLowerCase());
        }

        async function createClientRecord(clientName) {
            const response = await fetch('/api/clients', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ClientName: clientName })
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || 'Failed to create client');
            }

            const client = await response.json();
            allClients.push(client);
            refreshClientOptions(client.id);
            return client;
        }

        async function createServiceRecord(serviceName, serviceCost) {
            const response = await fetch('/api/services', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    ServiceName: serviceName,
                    Cost: parseFloat(serviceCost)
                })
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || 'Failed to create service');
            }

            const service = await response.json();
            allServices.push(service);
            refreshServiceOptions(service.id);
            return service;
        }

        async function getOrCreateClient(clientName) {
            const existingClient = findClientByName(clientName);
            if (existingClient) {
                return existingClient;
            }

            return createClientRecord(clientName);
        }

        async function getExpenseServiceId() {
            if (allServices.length > 0) {
                return allServices[0].id;
            }

            const expenseService = await createServiceRecord('General Expense', 0);
            return expenseService.id;
        }

        async function handleClientSubmit(e) {
            e.preventDefault();
            document.getElementById('clientError').textContent = '';
            document.getElementById('clientSuccess').textContent = '';

            const clientName = document.getElementById('clientName').value.trim();

            if (!clientName) {
                document.getElementById('clientError').textContent = 'Client name is required';
                return;
            }

            try {
                const existingClient = findClientByName(clientName);
                if (existingClient) {
                    document.getElementById('clientSuccess').textContent = `Client "${existingClient.ClientName}" already exists.`;
                    return;
                }

                const client = await createClientRecord(clientName);
                document.getElementById('clientSuccess').textContent = `Client "${client.ClientName}" created successfully.`;
                document.getElementById('clientForm').reset();
            } catch (error) {
                console.error('Error creating client:', error);
                document.getElementById('clientError').textContent = `Error: ${error.message}`;
            }
        }

        async function handleServiceSubmit(e) {
            e.preventDefault();
            document.getElementById('serviceError').textContent = '';
            document.getElementById('serviceSuccess').textContent = '';

            const serviceName = document.getElementById('serviceName').value.trim();
            const serviceCost = document.getElementById('serviceCost').value;

            if (!serviceName) {
                document.getElementById('serviceError').textContent = 'Service name is required';
                return;
            }

            if (!serviceCost || Number(serviceCost) < 0) {
                document.getElementById('serviceError').textContent = 'Valid cost is required';
                return;
            }

            try {
                const service = await createServiceRecord(serviceName, serviceCost);
                document.getElementById('serviceSuccess').textContent = `Service "${service.ServiceName}" created successfully.`;
                document.getElementById('serviceForm').reset();
            } catch (error) {
                console.error('Error creating service:', error);
                document.getElementById('serviceError').textContent = `Error: ${error.message}`;
            }
        }

        async function handleIncomeSubmit(e) {
            e.preventDefault();
            document.getElementById('incomeClientError').textContent = '';
            document.getElementById('incomeServiceError').textContent = '';

            const clientId = document.getElementById('incomeClient').value;
            const serviceId = document.getElementById('incomeService').value;

            if (!clientId) {
                document.getElementById('incomeClientError').textContent = 'Client is required';
                return;
            }

            if (!serviceId) {
                document.getElementById('incomeServiceError').textContent = 'Service is required';
                return;
            }

            try {
                const client = allClients.find(c => c.id === parseInt(clientId));

                const jobData = {
                    client_id: client.id,
                    job_date: document.getElementById('incomeDate').value,
                    service_id: parseInt(serviceId),
                    service_details: document.getElementById('incomeDetails').value || null,
                    income: parseFloat(document.getElementById('incomeAmount').value),
                    expenses: 0,
                    expense_notes: null,
                    status: 'Scheduled'
                };

                const jobResponse = await fetch('/api/jobs', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(jobData)
                });

                if (!jobResponse.ok) throw new Error('Failed to save job');

                const job = await jobResponse.json();
                addEntryToDisplay(job, 'income');
                document.getElementById('incomeForm').reset();
                setTodayDates();
                await updateSummary();
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('incomeClientError').textContent = `Error: ${error.message}`;
            }
        }

        async function handleExpenseSubmit(e) {
            e.preventDefault();
            document.getElementById('expenseClientError').textContent = '';

            const clientId = document.getElementById('expenseClient').value;

            if (!clientId) {
                document.getElementById('expenseClientError').textContent = 'Client is required';
                return;
            }

            try {
                const client = allClients.find(c => c.id === parseInt(clientId));
                const expenseServiceId = await getExpenseServiceId();

                const jobData = {
                    client_id: client.id,
                    job_date: document.getElementById('expenseDate').value,
                    service_id: expenseServiceId,
                    service_details: null,
                    income: 0,
                    expenses: parseFloat(document.getElementById('expenseAmount').value),
                    expense_notes: document.getElementById('expenseNotes').value || null,
                    status: 'Completed'
                };

                const jobResponse = await fetch('/api/jobs', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(jobData)
                });

                if (!jobResponse.ok) throw new Error('Failed to save expense');

                const job = await jobResponse.json();
                addEntryToDisplay(job, 'expense');
                document.getElementById('expenseForm').reset();
                setTodayDates();
                await updateSummary();
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('expenseClientError').textContent = `Error: ${error.message}`;
            }
        }

        async function loadRecentEntries() {
            try {
                const response = await fetch('/api/jobs');
                if (!response.ok) throw new Error('Failed to load recent entries');
                const jobs = await response.json();
                allEntries = jobs
                    .sort((a, b) => b.id - a.id)
                    .slice(0, 5)
                    .map(job => ({ ...job, type: job.income > 0 ? 'income' : 'expense' }));
                renderEntriesTable();
                await updateSummary();
            } catch (error) {
                console.error('Error loading recent entries:', error);
            }
        }

        function addEntryToDisplay(job, type) {
            allEntries.unshift({ ...job, type });
            if (allEntries.length > 5) allEntries = allEntries.slice(0, 5);
            renderEntriesTable();
        }

        function renderEntriesTable() {
            const entriesList = document.getElementById('entriesList');
            const recent = allEntries.slice(0, 5);

            if (recent.length === 0) {
                entriesList.innerHTML = '<div class="empty-state"><p>No entries yet. Add a job or expense above.</p></div>';
                return;
            }

            const rows = recent.map(entry => {
                const amount = entry.type === 'income' ? entry.income : entry.expenses;
                const clientName = allClients.find(c => c.id === entry.client_id)?.ClientName || 'Unknown';
                const description = entry.type === 'income'
                    ? (entry.service_details || clientName)
                    : (entry.expense_notes || 'Expense');
                const dateStr = formatDateShort(entry.job_date);
                const amountStr = amount.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
                return `
                    <tr data-job-id="${entry.id}" class="entry-row ${entry.type}">
                        <td>${dateStr}</td>
                        <td>${description}</td>
                        <td class="fw-bold">${amountStr}</td>
                        <td><button class="btn btn-sm btn-danger entry-delete" onclick="deleteEntry(${entry.id})">Delete</button></td>
                    </tr>`;
            }).join('');

            entriesList.innerHTML = `
                <table class="table table-striped table-bordered table-sm mb-0">
                    <thead class="table-dark">
                        <tr>
                            <th>Date</th>
                            <th>Description</th>
                            <th>Amount</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>${rows}</tbody>
                </table>`;
        }

        function formatDateShort(dateStr) {
            const [year, month, day] = dateStr.split('-');
            return `${month}/${day}/${year}`;
        }

        async function deleteEntry(jobId) {
            if (!confirm('Delete this entry?')) return;

            try {
                const response = await fetch(`/api/jobs/${jobId}`, { method: 'DELETE' });
                if (!response.ok) throw new Error('Failed to delete');

                allEntries = allEntries.filter(e => e.id !== jobId);
                renderEntriesTable();
                await updateSummary();
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to delete entry');
            }
        }

        async function updateSummary() {
            try {
                const response = await fetch('/api/jobs');
                if (!response.ok) throw new Error('Failed to load jobs');
                const jobs = await response.json();
                const totalIncome = jobs.reduce((sum, j) => sum + (j.income || 0), 0);
                const totalExpense = jobs.reduce((sum, j) => sum + (j.expenses || 0), 0);
                const netProfit = totalIncome - totalExpense;

                document.getElementById('totalIncomeAmount').textContent = totalIncome.toFixed(2);
                document.getElementById('totalExpenseAmount').textContent = totalExpense.toFixed(2);
                document.getElementById('netProfitAmount').textContent = netProfit.toFixed(2);
            } catch (error) {
                console.error('Error updating summary:', error);
            }
        }

        function formatDate(dateStr) {
            const date = new Date(dateStr + 'T00:00:00');
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        }
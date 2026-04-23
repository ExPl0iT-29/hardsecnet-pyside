let backend = null;

document.addEventListener("DOMContentLoaded", () => {
    // Initialize QWebChannel
    if (typeof qt !== 'undefined' && qt.webChannelTransport) {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            backend = channel.objects.backend;
            
            // Listen for signals from Python
            backend.snapshotUpdated.connect(function(payloadJson) {
                const payload = JSON.parse(payloadJson);
                renderDashboard(payload);
            });

            // Initial Data Fetch
            backend.getDashboardSnapshot(function(payloadJson) {
                const payload = JSON.parse(payloadJson);
                renderDashboard(payload);
            });
        });
    } else {
        console.warn("Qt WebChannel not found. Running in mock mode.");
        document.getElementById("device-details").innerText = "Not connected to Python backend.";
    }

    // UI Event Listeners
    document.getElementById("refresh-btn").addEventListener("click", () => {
        if (backend) backend.refreshSnapshot();
    });

    document.getElementById("run-btn").addEventListener("click", () => {
        const profileId = document.getElementById("profile-select").value;
        if (!profileId) return alert("Select a profile first.");
        
        const btn = document.getElementById("run-btn");
        btn.innerText = "Running...";
        btn.disabled = true;

        if (backend) {
            backend.runProfile(profileId, function(responseJson) {
                const response = JSON.parse(responseJson);
                if (response.error) alert("Error: " + response.error);
                btn.innerText = "Run Local Profile";
                btn.disabled = false;
            });
        }
    });
});

function renderDashboard(data) {
    if (data.error) {
        console.error(data.error);
        return;
    }

    // 1. Render Device Info
    document.getElementById("device-title").innerText = `${data.device.name} | ${data.device.os_family}`;
    document.getElementById("device-details").innerText = `${data.device.hostname} | ${data.items.length} controls loaded`;

    // 2. Render Profiles Dropdown
    const select = document.getElementById("profile-select");
    select.innerHTML = "";
    data.profiles.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.innerText = p.name;
        select.appendChild(opt);
    });

    // 3. Render Metrics
    const findings = data.findings || [];
    const compliantCount = findings.filter(f => f.status.toLowerCase() === 'compliant').length;
    const score = findings.length > 0 ? Math.round((compliantCount / findings.length) * 100) : 0;
    const openCount = findings.length - compliantCount;

    const metricsContainer = document.getElementById("metrics-container");
    metricsContainer.innerHTML = `
        <div class="metric-card" data-accent="green">
            <div class="metric-label">Compliance Score</div>
            <div class="metric-value">${score}%</div>
            <div class="metric-caption">${compliantCount}/${findings.length} compliant</div>
        </div>
        <div class="metric-card" data-accent="amber">
            <div class="metric-label">Open Findings</div>
            <div class="metric-value">${openCount}</div>
            <div class="metric-caption">Action required</div>
        </div>
        <div class="metric-card" data-accent="coral">
            <div class="metric-label">Drift Changes</div>
            <div class="metric-value">${data.comparisons ? data.comparisons.length : 0}</div>
            <div class="metric-caption">Since prior run</div>
        </div>
        <div class="metric-card" data-accent="blue">
            <div class="metric-label">Last Run</div>
            <div class="metric-value">${data.runs && data.runs.length > 0 ? 'OK' : 'None'}</div>
            <div class="metric-caption">Status</div>
        </div>
    `;

    // 4. Render Table
    const tbody = document.querySelector("#findings-table tbody");
    tbody.innerHTML = "";
    
    // Sort priority: Non-Compliant first
    const sorted = [...findings].sort((a, b) => {
        if (a.status === 'Non-Compliant' && b.status !== 'Non-Compliant') return -1;
        if (b.status === 'Non-Compliant' && a.status !== 'Non-Compliant') return 1;
        return 0;
    }).slice(0, 10); // Top 10

    sorted.forEach(f => {
        const tr = document.createElement("tr");
        
        let statusClass = 'status-compliant';
        if (f.status === 'Non-Compliant') statusClass = 'status-non-compliant';
        if (f.status === 'Needs Review') statusClass = 'status-needs-review';

        tr.innerHTML = `
            <td><strong>${f.benchmark_id}</strong></td>
            <td>${f.severity}</td>
            <td><span class="status-badge ${statusClass}">${f.status}</span></td>
            <td>${f.title}</td>
        `;
        tbody.appendChild(tr);
    });
}

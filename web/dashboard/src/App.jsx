import { useEffect, useState } from "react";
import { bootstrapAdmin, fetchJson, login } from "./api";

export default function App() {
  const [token, setToken] = useState("");
  const [summary, setSummary] = useState(null);
  const [reports, setReports] = useState([]);
  const [devices, setDevices] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        setError("");
        await bootstrapAdmin("admin", "admin");
        const auth = await login("admin", "admin");
        setToken(auth.access_token);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    }
    load();
  }, []);

  useEffect(() => {
    if (!token) return;
    async function loadData() {
      try {
        setError("");
        const [fleetSummary, reportList, deviceList, jobList, campaignList] = await Promise.all([
          fetchJson("/fleet/summary", token),
          fetchJson("/reports", token),
          fetchJson("/devices", token),
          fetchJson("/jobs", token),
          fetchJson("/campaigns", token)
        ]);
        setSummary(fleetSummary);
        setReports(reportList);
        setDevices(deviceList);
        setJobs(jobList);
        setCampaigns(campaignList);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    }
    loadData();
  }, [token]);

  return (
    <main className="app-shell">
      <section className="hero">
        <div>
          <p className="eyebrow">HardSecNet Control Plane</p>
          <h1>Fleet Security Dashboard</h1>
          <p>Live devices, jobs, approvals, reports, and comparison campaigns.</p>
        </div>
      </section>
      {error ? <div className="card error">{error}</div> : null}
      {loading ? <div className="card">Connecting to control plane...</div> : null}
      <section className="grid">
        <MetricCard label="Devices" value={summary?.active_device_count ?? devices.length} />
        <MetricCard label="Queued Jobs" value={summary?.queued_job_count ?? 0} />
        <MetricCard label="In Progress" value={summary?.in_progress_job_count ?? 0} />
        <MetricCard label="Completed" value={summary?.completed_job_count ?? 0} />
      </section>
      <section className="dashboard-layout">
        <Panel title="Devices">
          {devices.length === 0 ? <p>No enrolled devices yet.</p> :
          <table><thead><tr><th>Name</th><th>OS</th><th>Heartbeat</th><th>Pending</th></tr></thead>
            <tbody>{devices.map((row) => <tr key={row.device.id}><td>{row.device.name}</td><td>{row.device.os_family}</td><td>{row.heartbeat?.status ?? "unknown"}</td><td>{row.pending_jobs}</td></tr>)}</tbody>
          </table>}
        </Panel>
        <Panel title="Jobs">
          {jobs.length === 0 ? <p>No jobs yet.</p> :
          <table><thead><tr><th>ID</th><th>Device</th><th>Action</th><th>Status</th></tr></thead>
            <tbody>{jobs.map((job) => <tr key={job.id}><td>{job.id}</td><td>{job.device_id}</td><td>{job.action}</td><td>{job.status}</td></tr>)}</tbody>
          </table>}
        </Panel>
        <Panel title="Campaigns">
          {campaigns.length === 0 ? <p>No campaigns yet.</p> : <ul>{campaigns.map((campaign) => <li key={campaign.id}>{campaign.name} ({campaign.device_ids.length} devices)</li>)}</ul>}
        </Panel>
        <Panel title="Reports">
          {reports.length === 0 ? <p>No reports yet.</p> : <ul>{reports.map((report) => <li key={report.id}>{report.title}</li>)}</ul>}
        </Panel>
      </section>
    </main>
  );
}

function MetricCard({ label, value }) {
  return <div className="metric-card"><span>{label}</span><strong>{value}</strong></div>;
}

function Panel({ title, children }) {
  return <section className="card"><h2>{title}</h2>{children}</section>;
}

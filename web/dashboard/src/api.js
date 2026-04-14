const API_BASE = import.meta.env.VITE_HARDSECNET_API ?? "http://127.0.0.1:8000/api/v1";

export async function bootstrapAdmin(username, password) {
  const response = await fetch(`${API_BASE}/bootstrap/admin`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });
  if (!response.ok && response.status !== 400) {
    throw new Error(`Bootstrap failed: ${response.status}`);
  }
}

export async function login(username, password) {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });
  if (!response.ok) throw new Error(`Login failed: ${response.status}`);
  return response.json();
}

export async function fetchJson(path, token) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {}
  });
  if (!response.ok) {
    const body = await response.text().catch(() => "");
    throw new Error(`Request failed: ${path} (${response.status})${body ? ` ${body}` : ""}`);
  }
  return response.json();
}

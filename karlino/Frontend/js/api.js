async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("access");

  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  let res = await fetch(BASE_URL + endpoint, { ...options, headers });

  // اگه توکن منقضی شد، با refresh تازه‌اش کن و یک بار دیگه امتحان کن
  if (res.status === 401) {
    const refreshed = await tryRefreshToken();
    if (refreshed) {
      headers.Authorization = `Bearer ${localStorage.getItem("access")}`;
      res = await fetch(BASE_URL + endpoint, { ...options, headers });
    }
  }

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }

  return res.json();
}

async function tryRefreshToken() {
  const refresh = localStorage.getItem("refresh");
  if (!refresh) return false;

  const res = await fetch(BASE_URL + ENDPOINTS.refresh, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh }),
  });

  if (!res.ok) {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    return false;
  }

  const data = await res.json();
  localStorage.setItem("access", data.access);
  return true;
}
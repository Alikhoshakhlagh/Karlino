// config.js
const API_BASE = 'http://109.122.253.161:8000';

export const API = {
  REGISTER: `${API_BASE}/api/auth/register/`,
  LOGIN: `${API_BASE}/api/auth/login/`,
  REFRESH_TOKEN: `${API_BASE}/api/auth/token/refresh/`,
  FORGOT_PASSWORD: `${API_BASE}/api/auth/forgot-password/`,
  VERIFY_OTP: `${API_BASE}/api/auth/verify-otp/`,
  ME: `${API_BASE}/api/auth/profile/`,
  PROJECTS: `${API_BASE}/api/projects/`,
  PROJECT: (id) => `${API_BASE}/api/projects/${id}/`,
  CATEGORIES: `${API_BASE}/api/categories/`,
  SKILLS: `${API_BASE}/api/skills/`,
};
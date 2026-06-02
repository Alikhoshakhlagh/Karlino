export const BASE_URL = "http://localhost:8000"; // آدرس بک‌اند خودت

export const ENDPOINTS = {
  // auth
  login: "/api/auth/login/",
  register: "/api/auth/register/",
  refresh: "/api/auth/token/refresh/",
  profile: "/api/auth/profile/",
  forgotPassword: "/api/auth/forgot-password/",
  verifyOtp: "/api/auth/verify-otp/",

  // projects
  projects: "/api/projects/",
  myPosted: "/api/projects/my_posted/",

  // applications
  myApplications: "/api/applications/me/",
  incomingApplications: "/api/applications/incoming/",

  // others
  categories: "/api/categories/",
  skills: "/api/skills/",
  company: "/api/company/",
  favorites: "/api/favorites/",
};
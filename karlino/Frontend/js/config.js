const BASE_URL = "http://127.0.0.1:8000";

const ENDPOINTS = {
    // auth
    login: "/api/auth/login/",
    register: "/api/auth/register/",
    refresh: "/api/auth/token/refresh/",
    profile: "/api/auth/profile/",
    resetPassword: "/api/auth/resetpassword/",
    verifyOtp: "/api/auth/verify-otp/",
    dashboard: "/api/auth/dashboard/",
    charts: "/api/auth/profile/charts/",
    changePassword: "/api/auth/change-password/",
    sessions: "/api/auth/sessions/",

    // projects
    projects: "/api/projects/",
    myPosted: "/api/projects/my_posted/",
    myBids: "/api/projects/my-bids/",
    incomingBids: "/api/projects/incoming-bids/",

    // applications
    myApplications: "/api/applications/me/",
    incomingApplications: "/api/applications/incoming/",

    // others
    categories: "/api/categories/",
    skills: "/api/skills/",
    company: "/api/company/",
    favorites: "/api/favorites/",
};




// محافظت در برابر XSS: کاراکترهای خطرناک HTML را به معادل بی‌خطرشان تبدیل می‌کند
function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}
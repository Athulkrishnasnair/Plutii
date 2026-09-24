// credentials: "include" includes credentials as cookies while making a cross origin request

const API_KEY = 'http://localhost:5000/api';

async function request(endpoint, options = {}) {
    const response = await fetch(`${API_KEY}${endpoint}`, {
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        },
        ...options
    });

    const data = await response.json();

    // Check the response object
    if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
    }

    return data;
}

// Login function
export function login(credentials) {
    return request("/auth/login", {
        method: "POST",
        body: JSON.stringify(credentials)
    });
}

// Register
export function register(credentials) {
    return request("/auth/register", {
        method: "POST",
        body: JSON.stringify(credentials)
    });
}

// Get current user
export function getCurrentUser() {
    return request("/auth/me");
}

// Logout
export function logout() {
    return request("/auth/logout", {
        method: "POST"
    });
}
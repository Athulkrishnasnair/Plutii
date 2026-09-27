// Set URL
const API_URL = 'https://arrowlens.onrender.com/api';

// Wrapper function for request
async function req(endpoint, options = {}) {
    
    // Get a response
    const res = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        credentials: "include",
        headers: {
            // Default header
            "Content-Type": 'application/json',
            ...options.headers
        },
    });

    if (!res.ok) 
    {
        throw new Error(`Request failed: ${res.status}`)
    }
    const data = await res.json();
    return data
}




// Get Notes 
export function getNotes(){
    return req("/notes");
}

// Get Note
export function getNote(id){
    return req(`/notes/${id}`)
}

// Create note
export function createNote(note){
    return req("/notes", {
        method: "POST",
        body: JSON.stringify(note)
    });
};

// Update note
export function updateNote(id, note){
    return req(`/notes/${id}`, {
        method: "PUT",
        body: JSON.stringify(note)
    })
}

// Delete note
export function deleteNote(id){
    return req(`/notes/${id}`, {
        method: "DELETE"
    })
}

// Analyze a developer error
export function analyzeError(error, code = "", context = "") {
    return req("/analysis/error", {
        method: "POST",
        body: JSON.stringify({
            error,
            code,
            context
        })
    });
}

// Analyze Docs
export function analyzeDocs(content) {
    return req("/docs/analyze", {
        method: "POST",
        body: JSON.stringify({
            content
        })
    });
}

// Analyse plan
export function analyzePlan(content) {
    return req("/plan/analyze", {
        method: "POST",
        body: JSON.stringify({ content })
    });
}

// Get history
export function getAnalysisHistory() {
    return req("/analysis/history");
}

export function deleteAnalysis(id) {
    return req(`/analysis/${id}`, {
        method: "DELETE"
    });
}

// Scrape the docs
export function fetchDocsUrl(url) {
    return req("/docs/fetch", {
        method: "POST",
        body: JSON.stringify({ url })
    });
}

// Pass in the zip file
export function uploadCodebase(file) {
    const formData = new FormData();
    formData.append("file", file);

    return fetch(`${API_URL}/codebase/upload`, {
        method: "POST",
        credentials: "include",
        body: formData
    }).then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Upload failed.");
        }

        return data;
    });
}

// Import public GitHub repository
export function importGithubRepo(url) {
    return fetch(`${API_URL}/codebase/github`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url })
    }).then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "GitHub repository import failed.");
        }

        return data;
    });
}

// Analyze codebase

export function analyzeCodebase(query) {
    return fetch(`${API_URL}/codebase/analyze`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query })
    }).then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Analysis failed.");
        }

        return data;
    });
}

// Fetch single codebase file content
export function getCodebaseFile(path, codebaseId = null) {
    const params = new URLSearchParams({ path });
    if (codebaseId) {
        params.append("codebase_id", codebaseId);
    }

    return fetch(`${API_URL}/codebase/file?${params.toString()}`, {
        method: "GET",
        credentials: "include"
    }).then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to load file content.");
        }

        return data;
    });
}

// Explain a codebase file or selection
export function explainCodebaseCode(payload) {
    return fetch(`${API_URL}/codebase/explain`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    }).then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Code explanation failed.");
        }

        return data;
    });
}
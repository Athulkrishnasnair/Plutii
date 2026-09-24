// Set URL
const API_URL = 'http://localhost:5000/api';

// Wrapper function for request
async function req(endpoint, options = {}) {
    
    // Get a response
    const res = await fetch(`${API_URL}${endpoint}`, {
        credentials: "include",
        headers: {
            // Default header
            "Content-Type": 'application/json',
            ...options.headers
        },
        ...options
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
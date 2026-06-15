const API_BASE_URL = "http://localhost:8000/api";

export async function solveGame(payload) {
    const response = await fetch(`${API_BASE_URL}/solve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to solve game');
    }

    return response.json();
}

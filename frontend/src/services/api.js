const API_BASE_URL = 'http://127.0.0.1:8000'

export async function investigateLogs(logText) {
  const response = await fetch(`${API_BASE_URL}/investigate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      log_text: logText,
    }),
  })

  if (!response.ok) {
    throw new Error(`Investigation failed: ${response.status}`)
  }

  return response.json()
}

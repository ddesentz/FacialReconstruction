const headers = {
  Accept: "application/json",
  "Content-Type": "application/json",
  Options: "/api/task-items",
};

export async function get(endpoint: string) {
  return fetch(endpoint, {
    headers,
    method: "GET",
  });
}

export async function post(endpoint: string, body: any) {
  return fetch(endpoint, {
    body: JSON.stringify(body),
    headers,
    method: "POST",
  });
}

export async function update(endpoint: string, body: any) {
  return fetch(endpoint, {
    body: JSON.stringify(body),
    headers,
    method: "PUT",
  });
}

export async function destroy(endpoint: string, id: number) {
  const url = `${endpoint}/${id}`;
  return fetch(url, {
    method: "DELETE",
  });
}

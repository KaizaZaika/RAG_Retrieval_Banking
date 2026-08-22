import { api } from "./client";

export async function registerUser(
  username: string,
  email: string,
  password: string
) {
  const response = await api.post("/auth/register", {
    username,
    email,
    password,
  });

  return response.data;
}

export async function loginUser(
  email: string,
  password: string
) {
  const response = await api.post("/auth/login", {
    email,
    password,
  });

  return response.data;
}

export async function getMe(token: string) {
  const response = await api.get("/auth/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
}

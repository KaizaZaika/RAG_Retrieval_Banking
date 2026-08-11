import { useEffect, useState } from "react";

import { getMe } from "../api";

type User = {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
};

type Props = {
  token: string;
};

export default function ProfilePage({ token }: Props) {
  const [user, setUser] = useState<User | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function loadUser() {
      try {
        const result = await getMe(token);
        setUser(result);
      } catch (error) {
        setMessage(
          error instanceof Error
            ? error.message
            : "Could not load user"
        );
      }
    }

    if (token) {
      loadUser();
    }
  }, [token]);

  if (!token) {
    return <p>Please login first.</p>;
  }

  return (
    <main>
      <h1>Profile</h1>

      {message && <p>{message}</p>}

      {user && (
        <div>
          <p>ID: {user.id}</p>
          <p>Username: {user.username}</p>
          <p>Email: {user.email}</p>
          <p>
            Active: {user.is_active ? "Yes" : "No"}
          </p>
          <p>Role: {user.role}</p>
        </div>
      )}
    </main>
  );
}

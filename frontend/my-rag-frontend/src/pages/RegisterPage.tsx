import { useState } from "react";
import { Link } from "react-router-dom";

import { registerUser } from "../api";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  async function handleRegister() {
    try {
      const user = await registerUser(
        username,
        email,
        password
      );

      setMessage(`Registered ${user.username}`);
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Registration failed"
      );
    }
  }

  return (
    <main>
      <h1>Register</h1>

      <input
        placeholder="Username"
        value={username}
        onChange={(event) =>
          setUsername(event.target.value)
        }
      />

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(event) =>
          setEmail(event.target.value)
        }
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(event) =>
          setPassword(event.target.value)
        }
      />

      <button onClick={handleRegister}>
        Register
      </button>

      {message && <p>{message}</p>}

      <p>
        Already have an account?{" "}
        <Link to="/login">Login</Link>
      </p>
    </main>
  );
}

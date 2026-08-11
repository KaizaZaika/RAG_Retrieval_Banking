import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { loginUser } from "../api";

type Props = {
  onLogin: (token: string) => void;
};

export default function LoginPage({ onLogin }: Props) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  async function handleLogin() {
    try {
      const result = await loginUser(
        email,
        password
      );

      onLogin(result.access_token);
      navigate("/me");
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Login failed"
      );
    }
  }

  return (
    <main>
      <h1>Login</h1>

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

      <button onClick={handleLogin}>
        Login
      </button>

      {message && <p>{message}</p>}

      <p>
        No account?{" "}
        <Link to="/register">Register</Link>
      </p>
    </main>
  );
}

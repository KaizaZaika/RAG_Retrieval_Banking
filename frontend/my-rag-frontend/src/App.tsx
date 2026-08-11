import { useState } from "react";
import {
  Link,
  Navigate,
  Route,
  Routes,
  useNavigate,
} from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import ProfilePage from "./pages/ProfilePage";
import RegisterPage from "./pages/RegisterPage";

export default function App() {
  const [token, setToken] = useState("");
  const navigate = useNavigate();

  function handleLogout() {
    setToken("");
    navigate("/login");
  }

  return (
    <>
      <nav>
        {!token ? (
          <>
            <Link to="/register">Register</Link>
            {" | "}
            <Link to="/login">Login</Link>
          </>
        ) : (
          <>
            <Link to="/me">Me</Link>
            {" | "}
            <button onClick={handleLogout}>Logout</button>
          </>
        )}
      </nav>

      <Routes>
        <Route
          path="/"
          element={
            <Navigate
              to={token ? "/me" : "/login"}
              replace
            />
          }
        />

        <Route
          path="/register"
          element={
            token
              ? <Navigate to="/me" replace />
              : <RegisterPage />
          }
        />

        <Route
          path="/login"
          element={
            token
              ? <Navigate to="/me" replace />
              : <LoginPage onLogin={setToken} />
          }
        />

        <Route
          path="/me"
          element={
            token
              ? <ProfilePage token={token} />
              : <Navigate to="/login" replace />
          }
        />
      </Routes>
    </>
  );
}

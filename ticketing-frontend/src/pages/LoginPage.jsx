import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { apiRequest } from "../api/client";
import { isLoggedIn, saveTokens, saveUsername } from "../api/auth";
import { getErrorMessage } from "../api/errors";

export default function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const alreadyLoggedIn = isLoggedIn();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!alreadyLoggedIn) return;

    const timer = setTimeout(() => {
      navigate("/", { replace: true });
    }, 2000);

    return () => clearTimeout(timer);
  }, [alreadyLoggedIn, navigate]);

  async function handleSubmit(event) {
    event.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const data = await apiRequest("/api/auth/token/", {
        method: "POST",
        body: JSON.stringify({
          username,
          password,
        }),
      });

      saveTokens(data);
      saveUsername(username);
      const redirectTo = location.state?.from || "/";
      navigate(redirectTo);
    } catch (err) {
      if (err.status === 401) {
        setError("Invalid username or password.");
      } else {
        setError(
          getErrorMessage(
            err,
            "Unable to log in. Please try again."
          )
        );
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  if (alreadyLoggedIn) {
    return (
      <main>
        <h1>Log in</h1>

        <p className="form-error">You are already logged in.</p>

        <p>Redirecting you to the home page…</p>
      </main>
    );
  }

  return (
    <main>
      <h1>Log in</h1>
      {location.state?.message && (
        <p className="form-error">{location.state.message}</p>
      )}

      <form className="form" onSubmit={handleSubmit}>
        <div className="form-field">
          <label className="form-label" htmlFor="username">
            Username
          </label>

          <input
            className="form-input"
            id="username"
            type="text"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            required
          />
        </div>

        <div className="form-field">
          <label className="form-label" htmlFor="password">
            Password
          </label>

          <input
            className="form-input"
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </div>

        {error && <p className="form-error">{error}</p>}

        <button className="button" type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Logging in…" : "Log in"}
        </button>

        <p>
          Need an account? <Link to="/register">Register</Link>
        </p>
      </form>
    </main>
  );
}
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiRequest } from "../api/client";
import { isLoggedIn } from "../api/auth";
import { getErrorMessage } from "../api/errors";

export default function RegisterPage() {
  const navigate = useNavigate();

  const alreadyLoggedIn = isLoggedIn();
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    date_of_birth: "",
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!alreadyLoggedIn) return;

    const timer = setTimeout(() => {
      navigate("/", { replace: true });
    }, 2000);

    return () => clearTimeout(timer);
  }, [alreadyLoggedIn, navigate]);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError(null);

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setIsSubmitting(true);

    try {
      await apiRequest("/api/auth/register/", {
        method: "POST",
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          date_of_birth: formData.date_of_birth || null,
        }),
      });

      navigate("/login", {
        state: {
          message: "Account created. Please log in.",
        },
      });
    } catch (err) {
      setError(
        getErrorMessage(
          err,
          "Unable to create account. Please try again."
        )
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  if (alreadyLoggedIn) {
    return (
      <main>
        <h1>Create account</h1>

        <p className="form-error">You are already logged in.</p>

        <p>Redirecting you to the home page…</p>
      </main>
    );
  }

  return (
    <main>
      <h1>Create account</h1>

      <form className="form" onSubmit={handleSubmit}>
        <div className="form-field">
          <label className="form-label" htmlFor="username">
            Username
          </label>

          <input
            className="form-input"
            id="username"
            name="username"
            type="text"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-field">
          <label className="form-label" htmlFor="email">
            Email
          </label>

          <input
            className="form-input"
            id="email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
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
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-field">
          <label className="form-label" htmlFor="confirmPassword">
            Confirm password
          </label>

          <input
            className="form-input"
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-field">
          <label className="form-label" htmlFor="date_of_birth">
            Date of birth
          </label>

          <input
            className="form-input"
            id="date_of_birth"
            name="date_of_birth"
            type="date"
            value={formData.date_of_birth}
            onChange={handleChange}
          />
        </div>

        {error && <p className="form-error">{error}</p>}

        <button className="button" type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Creating account…" : "Create account"}
        </button>

        <p>
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </form>
    </main>
  );
}
import { Navigate, useLocation } from "react-router-dom";
import { isLoggedIn } from "../api/auth";

export default function RequireAuth({ children }) {
  const location = useLocation();

  if (!isLoggedIn()) {
    return (
      <Navigate
        to="/login"
        replace
        state={{
          from: location.pathname,
          message: "Please log in to continue.",
        }}
      />
    );
  }

  return children;
}
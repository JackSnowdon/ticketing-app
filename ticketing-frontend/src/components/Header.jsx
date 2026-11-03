import { useEffect, useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { 
  isLoggedIn, 
  logout, 
  getUsername, 
  fetchCurrentUser
} from "../api/auth";

export default function Header() {
  const location = useLocation();
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());
  const [username, setUsername] = useState(getUsername());
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    setLoggedIn(isLoggedIn());
    setUsername(getUsername());

    async function loadCurrentUser() {
      if (!isLoggedIn()) {
        setCurrentUser(null);
        return;
      }

      try {
        const user = await fetchCurrentUser();
        setCurrentUser(user);
      } catch (err) {
        setCurrentUser(null);
      }
    }

    loadCurrentUser();
  }, [location]);

  function handleLogout() {
    logout();
    setLoggedIn(false);
    setUsername(null);
    setCurrentUser(null);
  }

  return (
    <header className="site-header">
      <div className="site-header-inner">
        <NavLink to="/" className="brand">
          TicketFast
        </NavLink>

        <nav className="site-nav">
          <NavLink
            to="/"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Events
          </NavLink>

          {loggedIn && (
            <NavLink
              to="/my-bookings"
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
            >
              My bookings
            </NavLink>
          )}

          {loggedIn && (currentUser?.username || username) && (
            <span className="logged-in-as">
              Logged in as {currentUser?.username || username}
            </span>
          )}

          {loggedIn ? (
            <button className="nav-button" onClick={handleLogout}>
              Log out
            </button>
          ) : (
            <>
              <NavLink
                to="/login"
                className={({ isActive }) =>
                  isActive ? "nav-link active" : "nav-link"
                }
              >
                Log in
              </NavLink>

              <NavLink
                to="/register"
                className={({ isActive }) =>
                  isActive ? "nav-link active" : "nav-link"
                }
              >
                Register
              </NavLink>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
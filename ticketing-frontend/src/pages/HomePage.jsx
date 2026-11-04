import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../api/client";
import { isLoggedIn } from "../api/auth";
import EventCard from "../components/EventCard";

export default function HomePage() {
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());

  useEffect(() => {
    setLoggedIn(isLoggedIn());

    async function loadFeaturedEvents() {
      try {
        const data = await apiRequest("/api/events/");
        setEvents(data.results.slice(0, 3));
      } catch (err) {
        setError("Unable to load upcoming events.");
      } finally {
        setIsLoading(false);
      }
    }

    loadFeaturedEvents();
  }, []);

  return (
    <main>
      <section className="home-hero">
        <div className="home-hero-content">
          <p className="home-eyebrow">Live events, made simple</p>

          <h1>Find your next night out</h1>

          <p className="home-lede">
            Browse upcoming events, check live ticket availability, and book
            your place in seconds.
          </p>

          <div className="home-actions">
            <Link to="/events" className="button button-primary">
              Browse events
            </Link>

            {loggedIn ? (
              <Link to="/my-bookings" className="button button-secondary">
                My bookings
              </Link>
            ) : (
              <Link to="/register" className="button button-secondary">
                Create an account
              </Link>
            )}
          </div>
        </div>
      </section>

      <section className="home-featured">
        <div className="home-section-header">
          <h2>Next upcoming shows</h2>

          <Link to="/events" className="home-view-all">
            View all events
          </Link>
        </div>

        {isLoading && <p className="loading-message">Loading events…</p>}

        {error && <p className="error-message">{error}</p>}

        {!isLoading && !error && events.length === 0 && (
          <p>No upcoming events are available right now.</p>
        )}

        {!isLoading && !error && events.length > 0 && (
          <ul className="event-list">
            {events.map((event) => (
              <EventCard key={event.id} event={event} />
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
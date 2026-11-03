import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../api/client";

import EventCard from "../components/EventCard";

export default function EventsPage() {
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadEvents() {
      try {
        const data = await apiRequest("/api/events/");
        setEvents(data.results);
      } catch (err) {
        setError("Unable to load events.");
      } finally {
        setIsLoading(false);
      }
    }

    loadEvents();
  }, []);

  if (isLoading) {
    return <p className="loading-message">Loading events…</p>;
  }

  if (error) {
    return <p className="error-message">{error}</p>;
  }

  return (
    <main>
      <h1>Upcoming events</h1>
      <p className="event-meta">
        Browse events and choose one to see available tickets.
      </p>

      {events.length === 0 ? (
        <p>No upcoming events are available.</p>
      ) : (
        <ul className="event-list">
          {events.map((event) => (
            <EventCard key={event.id} event={event} />
          ))}
        </ul>
      )}
    </main>
  );
}
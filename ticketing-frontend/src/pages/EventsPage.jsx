import { useEffect, useState } from "react";
import { apiRequest } from "../api/client";

export default function EventsPage() {
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadEvents() {
      try {
        const data = await apiRequest("/tickets/events/");
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
    return <p>Loading events…</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <main>
      <h1>Upcoming events</h1>

      {events.length === 0 ? (
        <p>No upcoming events are available.</p>
      ) : (
        <ul>
          {events.map((event) => (
            <li key={event.id}>
              <h2>{event.title}</h2>
              <p>
                {event.venue.name}, {event.venue.city}
              </p>
              <p>
                Starts: {new Date(event.starts_at).toLocaleString()}
              </p>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
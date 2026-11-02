import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { apiRequest } from "../api/client";

export default function EventDetailPage() {
  const { id } = useParams();
  const [event, setEvent] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadEvent() {
      try {
        const data = await apiRequest(`/tickets/events/${id}/`);
        setEvent(data);
      } catch (err) {
        setError("Unable to load this event.");
      } finally {
        setIsLoading(false);
      }
    }

    loadEvent();
  }, [id]);

  if (isLoading) {
    return <p className="loading-message">Loading event…</p>;
  }

  if (error) {
    return (
      <main>
        <p className="error-message">{error}</p>
        <Link className="back-link" to="/">
          Back to events
        </Link>
      </main>
    );
  }

  return (
    <main>
      <Link className="back-link" to="/">
        Back to events
      </Link>

      <h1>{event.title}</h1>

      <p className="event-meta">
        {event.venue.name}, {event.venue.city}
      </p>

      <p>Starts: {new Date(event.starts_at).toLocaleString()}</p>

      {event.ends_at && (
        <p>Ends: {new Date(event.ends_at).toLocaleString()}</p>
      )}

      {event.description && <p>{event.description}</p>}

      <h2>Ticket types</h2>

      {event.ticket_types.length === 0 ? (
        <p>No ticket types are available for this event.</p>
      ) : (
        <ul className="ticket-list">
          {event.ticket_types.map((ticketType) => (
            <li className="ticket-item" key={ticketType.id}>
              <strong>{ticketType.name}</strong>
              <p className="event-meta">
                Price: £{ticketType.price}
                <br />
                Available: {ticketType.quantity_available}
              </p>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
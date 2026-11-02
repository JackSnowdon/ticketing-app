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
    return <p>Loading event…</p>;
  }

  if (error) {
    return (
      <main>
        <p>{error}</p>
        <Link to="/">Back to events</Link>
      </main>
    );
  }

  return (
    <main>
      <Link to="/">Back to events</Link>

      <h1>{event.title}</h1>
      <p>
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
        <ul>
          {event.ticket_types.map((ticketType) => (
            <li key={ticketType.id}>
              <strong>{ticketType.name}</strong>
              <br />
              Price: £{ticketType.price}
              <br />
              Available: {ticketType.quantity_available}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
import { Link } from "react-router-dom";

export default function EventCard({ event }) {
  return (
    <li className="event-card">
      <Link to={`/events/${event.id}`}>
        <h2>{event.title}</h2>
      </Link>

      <p className="event-meta">
        {event.venue.name}, {event.venue.city}
      </p>

      <p className="event-meta">
        Starts: {new Date(event.starts_at).toLocaleString()}
      </p>
    </li>
  );
}
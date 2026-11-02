import { Link, useLocation, useParams } from "react-router-dom";

export default function BookingPage() {
  const { id } = useParams();
  const location = useLocation();

  const bookingDetails = location.state;

  if (!bookingDetails) {
    return (
      <main>
        <h1>Booking</h1>
        <p>No ticket type was selected.</p>
        <Link className="back-link" to={`/events/${id}`}>
          Back to event
        </Link>
      </main>
    );
  }

  return (
    <main>
      <h1>Booking</h1>

      <p>
        You selected ticket type ID:{" "}
        <strong>{bookingDetails.ticketTypeId}</strong>
      </p>

      <p>
        For event ID: <strong>{bookingDetails.eventId}</strong>
      </p>

      <p>This page will soon collect attendee details and create a booking.</p>

      <Link className="back-link" to={`/events/${id}`}>
        Back to event
      </Link>
    </main>
  );
}
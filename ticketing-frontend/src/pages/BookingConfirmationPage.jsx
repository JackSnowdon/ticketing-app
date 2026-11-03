import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { apiRequest } from "../api/client";

export default function BookingConfirmationPage() {
  const { reference } = useParams();

  const [booking, setBooking] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadBooking() {
      try {
        const data = await apiRequest(`/api/bookings/${reference}/`);
        setBooking(data);
      } catch (err) {
        setError("Unable to load your booking.");
      } finally {
        setIsLoading(false);
      }
    }

    loadBooking();
  }, [reference]);

  if (isLoading) {
    return <p className="loading-message">Loading your booking…</p>;
  }

  if (error) {
    return (
      <main>
        <p className="error-message">{error}</p>
        <Link className="back-link" to="/my-bookings">
          Back to My Bookings
        </Link>
      </main>
    );
  }

  return (
    <main>
      <div className="confirmation-banner">
        <h1>Booking confirmed</h1>
        <p>
          Your booking reference is <strong>{booking.reference}</strong>.
        </p>
      </div>

      <h2>Booking details</h2>

      <p>
        Status: <strong>{booking.status}</strong>
      </p>

      <ul className="ticket-list">
        {booking.items.map((item) => (
          <li className="ticket-item" key={item.id}>
            <strong>{item.event_title}</strong>
            <p className="event-meta">
              {item.ticket_type_name}
              <br />
              Quantity: {item.quantity}
              <br />
              Price each: £{item.unit_price}
              <br />
              Line total: £{item.line_total}
            </p>
          </li>
        ))}
      </ul>

      <p className="booking-total">
        Total: £{booking.total}
      </p>

      <Link className="back-link" to="/my-bookings">
        View all bookings
      </Link>
    </main>
  );
}
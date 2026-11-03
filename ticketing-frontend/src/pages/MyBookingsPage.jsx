import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { apiRequest } from "../api/client";

export default function MyBookingsPage() {
  const location = useLocation();
  const confirmation = location.state?.confirmation;

  const [bookings, setBookings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [cancellingReference, setCancellingReference] = useState(null);
  const [cancelError, setCancelError] = useState(null);

  useEffect(() => {
    async function loadBookings() {
      try {
        const data = await apiRequest("/api/bookings/");
        setBookings(data.results);
      } catch (err) {
        setError("Unable to load your bookings.");
      } finally {
        setIsLoading(false);
      }
    }

    loadBookings();
  }, []);

  async function handleCancelBooking(reference) {
    setCancellingReference(reference);
    setCancelError(null);

    try {
      const updatedBooking = await apiRequest(
        `/api/bookings/${reference}/cancel/`,
        {
          method: "POST",
        }
      );

      setBookings((previousBookings) =>
        previousBookings.map((booking) =>
          booking.reference === reference ? updatedBooking : booking
        )
      );
    } catch (err) {
      if (err.data?.detail) {
        setCancelError(err.data.detail);
      } else {
        setCancelError("Unable to cancel this booking.");
      }
    } finally {
      setCancellingReference(null);
    }
  }

  if (isLoading) {
    return <p className="loading-message">Loading your bookings…</p>;
  }

  if (error) {
    return <p className="error-message">{error}</p>;
  }

  return (
    <main>
      <h1>My bookings</h1>

      {cancelError && (
        <p className="form-error">{cancelError}</p>
      )}

      {confirmation && (
        <div className="confirmation-banner">
          <h2>Booking confirmed</h2>
          <p>
            Your booking reference is <strong>{confirmation.reference}</strong>.
          </p>
          <p>
            Total: £{confirmation.total}
          </p>
        </div>
      )}

      {bookings.length === 0 ? (
        <p>
          You have no bookings yet.{" "}
          <Link to="/">Browse events</Link>
        </p>
      ) : (
        <ul className="booking-list">
          {bookings.map((booking) => (
            <li className="booking-card" key={booking.id}>
              <div className="booking-header">
                <h2>{booking.reference}</h2>
                <span className={`status status-${booking.status}`}>
                  {booking.status}
                </span>
              </div>

              <ul className="ticket-list">
                {booking.items.map((item) => (
                  <li className="ticket-item" key={item.id}>
                    <strong>{item.event_title}</strong>
                    <p className="event-meta">
                      {item.ticket_type_name}
                      <br />
                      Quantity: {item.quantity}
                      <br />
                      Line total: £{item.line_total}
                    </p>
                  </li>
                ))}
              </ul>

              <p className="booking-total">
                Total: £{booking.total}
              </p>
                {booking.status !== "cancelled" && (
                  <button
                    className="button button-danger"
                    onClick={() => handleCancelBooking(booking.reference)}
                    disabled={cancellingReference === booking.reference}
                  >
                    {cancellingReference === booking.reference
                      ? "Cancelling…"
                      : "Cancel booking"}
                  </button>
                )}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
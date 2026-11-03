import { useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { apiRequest } from "../api/client";
import { getErrorMessage } from "../api/errors";

export default function BookingPage() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const bookingDetails = location.state;

  const [quantity, setQuantity] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

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

  async function handleSubmit(event) {
    event.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const data = await apiRequest("/api/bookings/", {
        method: "POST",
        body: JSON.stringify({
          ticket_type_id: bookingDetails.ticketTypeId,
          quantity: quantity,
        }),
      });

      navigate(`/bookings/${data.reference}/confirmation`);
    } catch (err) {
      if (err.status === 401) {
        navigate("/login", {
          state: {
            from: `/events/${id}/book`,
            message: "Please log in to complete your booking.",
          },
        });
        return;
      } else {
        setError(
          getErrorMessage(
            err,
            "Unable to create booking. Please try again."
          )
        );
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main>
      <h1>Booking</h1>

      {bookingDetails.ticketType ? (
        <div className="selected-ticket">
          <h2>{bookingDetails.ticketType.name}</h2>
          <p className="event-meta">
            Price: £{bookingDetails.ticketType.price}
            <br />
            Available: {bookingDetails.ticketType.quantity_available}
          </p>
        </div>
      ) : (
        <p>
          You selected ticket type ID:{" "}
          <strong>{bookingDetails.ticketTypeId}</strong>
        </p>
      )}

      <form className="form" onSubmit={handleSubmit}>
        <div className="form-field">
          <label className="form-label" htmlFor="quantity">
            Number of tickets
          </label>

          <input
            className="form-input"
            id="quantity"
            type="number"
            min="1"
            value={quantity}
            onChange={(event) => setQuantity(Number(event.target.value))}
          />
        </div>

        {error && <p className="form-error">{error}</p>}

        <button className="button" type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Creating booking…" : "Confirm booking"}
        </button>
      </form>

      <Link className="back-link" to={`/events/${id}`}>
        Back to event
      </Link>
    </main>
  );
}
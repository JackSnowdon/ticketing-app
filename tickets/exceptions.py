class TicketingError(Exception):
    """Base exception for ticketing business rules."""


class InsufficientTicketsError(TicketingError):
    pass


class InvalidQuantityError(TicketingError):
    pass


class EventNotPublishedError(TicketingError):
    pass
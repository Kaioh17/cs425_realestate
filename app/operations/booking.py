"""
booking.py

Responsibilities:
- Create and manage property bookings (select property, rental period, payment method).
- Calculate total cost for booking periods and persist booking records.
- Allow renters and agents to view and cancel bookings; handle refund routing.
"""

# Implementation notes:
# - Integrate with Payment and Property models; record payment method and status.
# - Enforce availability checks before creating a booking.

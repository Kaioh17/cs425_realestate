"""
renters.py

Responsibilities:
- Renter account workflows: registration and profile management.
- Manage renter payment methods and addresses (add/modify/delete), enforcing rules
	such as "billing address cannot be deleted if associated with a card".
- Allow renters to view and cancel their bookings.
"""

# Implementation notes:
# - Use secure storage for payment metadata (do not store raw card numbers).
# - Validate address/payment relationships before delete operations.

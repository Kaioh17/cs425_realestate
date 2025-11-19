"""
agent.py

Responsibilities:
- Agents: create, update, and delete property listings.
- Provide endpoints/operations for agents to view bookings for their properties.
- Validate agent ownership and enforce agent-specific business rules.
"""

# Implementation notes:
# - Use DB models for Property and Booking.
# - Ensure actions check the agent's `user_id`/role before modifying data.

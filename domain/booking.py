class Booking:
    VALID_STATES = {"Pending", "Confirmed", "Cancelled"}

    def __init__(self, booking_id, room_id, guest_name):
        self.booking_id = booking_id
        self.room_id = room_id
        self.guest_name = guest_name
        self.status = "Pending"

    def confirm(self):
        if self.status != "Pending":
            raise ValueError(
                f"Cannot confirm a booking with status '{self.status}'"
            )

        self.status = "Confirmed"

    def cancel(self):
        if self.status != "Pending":
            raise ValueError(
                f"Cannot cancel a booking with status '{self.status}'"
            )

        self.status = "Cancelled"

        
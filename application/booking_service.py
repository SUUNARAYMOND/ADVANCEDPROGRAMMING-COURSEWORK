from application.dto import MakeBookingRequest, MakeBookingResult
from application.event_handling import BookingConfirmedHandler
from application.repositories import BookingRepository, RoomRepository
from domain.booking import Booking
from domain.booking_dates import BookingDates
from domain.booking_pricing_service import BookingPricingService


class BookingService:
    """Main use case: make a booking. It coordinates; the domain decides.

    Flow: look up Room (BR6) -> build dates (BR1) -> price (BR4) ->
    create and confirm Booking (BR2) -> hand the BookingConfirmed event to the
    handler (BR5) -> Room accepts or rejects (BR3) -> save Booking only if
    the follow-up was accepted.

    Repositories and the handler are supplied from outside (dependency
    injection), so this class never imports Infrastructure.
    """

    def __init__(
        self,
        room_repository: RoomRepository,
        booking_repository: BookingRepository,
        confirmed_handler: BookingConfirmedHandler,
    ) -> None:
        self._rooms = room_repository
        self._bookings = booking_repository
        self._confirmed_handler = confirmed_handler

    def make_booking(self, request: MakeBookingRequest) -> MakeBookingResult:
        room = self._rooms.get(request.room_id)  # BR6 lookup
        if room is None:
            return MakeBookingResult(False, f"Room '{request.room_id}' not found")

        try:
            dates = BookingDates(request.check_in, request.check_out)  # BR1
            total_price = BookingPricingService.calculate_price(  # BR4
                room.nightly_price, dates.nights
            )
            booking = Booking(
                request.booking_id,
                request.room_id,
                request.guest_name,
                dates,
                total_price,
            )
            event = booking.confirm()  # BR2
        except ValueError as error:
            return MakeBookingResult(False, str(error))

        outcome = self._confirmed_handler.handle(event)  # BR5 -> Room (BR3)
        if not outcome.accepted:
            # Do not store the attempted Booking when Room rejects reservation.
            return MakeBookingResult(
                False, f"Room rejected the reservation: {outcome.reason}"
            )

        self._bookings.save(booking)
        return MakeBookingResult(
            True,
            "Booking confirmed",
            booking_id=booking.booking_id,
            booking_status=booking.status.value,
            total_price=booking.total_price,
        )

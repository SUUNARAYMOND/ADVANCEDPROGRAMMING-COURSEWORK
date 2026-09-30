from decimal import Decimal, InvalidOperation


class BookingPricingService:
    """BR4: combine a room's nightly rate with the stay's number of nights."""

    @staticmethod
    def calculate_price(room_price, nights: int) -> Decimal:
        if type(nights) is not int or nights <= 0:
            raise ValueError("Number of nights must be a positive integer")

        try:
            nightly_price = Decimal(str(room_price))
        except InvalidOperation as error:
            raise ValueError("Nightly price must be a finite non-negative number") from error

        if not nightly_price.is_finite() or nightly_price < 0:
            raise ValueError("Nightly price must be a finite non-negative number")

        return nightly_price * nights

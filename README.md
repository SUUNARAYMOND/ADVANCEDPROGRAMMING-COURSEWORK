# Hotel Room Booking Coursework

Small Python implementation of DDD, TDD and Clean Architecture using
in-memory persistence. The project is under development by four members.

## Run the tests

```powershell
py -m pip install -r requirements.txt
py -m pytest -q
```

On systems with Python available as `python`, substitute `python` for `py`.

## Member 1: Booking aggregate

`Booking(booking_id, room_id, guest_name, dates, total_price)` stores the
booking data. Supply validated `BookingDates` from Member 2 and the price
calculated by `BookingPricingService`. Booking does not validate dates,
calculate prices, look up rooms or reserve them.

`BookingStatus` defines `PENDING`, `CONFIRMED` and `CANCELLED`, with values
`Pending`, `Confirmed` and `Cancelled`. Use `booking.status.value` for display.
The status property is read-only; transitions use the aggregate methods:

- `confirm()` allows only Pending -> Confirmed and returns one immutable
  `BookingConfirmed(booking_id, room_id, dates)` event.
- `cancel()` allows only Pending -> Cancelled.
- Either method raises `ValueError` for a terminal booking and preserves its
  existing status. A rejected confirmation returns no event.

Member 3's application service must capture the event returned by `confirm()`
and pass it to Member 4's in-process handler. The handler retrieves the Room
and calls the agreed `Room.reserve(booking_id, dates)` method. Member 2 and
Member 4 must use this same reservation signature. Booking never modifies Room.
The event contract is defined; its handler is still to be implemented.

T2 currently uses a date stand-in because Member 2's `BookingDates` is not
implemented. Replace that stand-in with the real value object when available.
The rest of the domain, application, infrastructure and interface remain
placeholders; only T2 is currently implemented. This is not yet a complete
eight-test coursework submission.

## TDD evidence for the Member 1 patch

The strengthened T2 was written and run before the patch. It failed because
Booking did not accept dates. After adding the required booking fields,
status enum and confirmation event, the same test passed.

- `evidence/member1-red.txt`: actual failing output from
  `py -m pytest tests/test_br2.py -q` before implementation.
- `evidence/member1-green.txt`: actual passing output from
  `py -m pytest -q` after implementation.

These files document this patch's cycle, not the original development of BR2.

## Integration decision still required

For T8, the team must agree on Booking's final state when Room rejects a
reservation. Under the current BR2 contract, a confirmed booking cannot be
cancelled. Room must preserve its existing reservations and the application
must report the failed follow-up. No rollback policy is implemented yet.

AI use: OpenAI Codex reviewed and patched the Booking aggregate, shared event
contract, T2, dependency setup and documentation.

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

T2 now uses Member 2's real `BookingDates` value object.

## Member 2: Room and domain logic

- BR1: `BookingDates(check_in, check_out)` takes `datetime.date` values and
  rejects checkout on or before check-in with `ValueError`. It is immutable
  and compares by its values; it has no separate identity. `dates.nights`
  gives the stay length. One night is the minimum valid stay.
- BR3: `Room(room_id, room_number, room_type, nightly_price)` is the second
  aggregate root. `room.reserve(booking_id, dates)` rejects overlapping
  reservations with `ValueError`, leaving all existing reservations unchanged.
  Check-in is inclusive and checkout exclusive: October 1-4 and October 4-6
  do not conflict. Overlap is `new_start < existing_end` and
  `existing_start < new_end`.
- Room owns immutable `Reservation(booking_id, dates)` records. They reference
  Booking by ID and do not hold or modify the Booking aggregate. Inspect them
  through the read-only tuple `room.reservations`; only Room adds records.
  All stored records are active reservations; reservation cancellation is
  outside the current scope.
- BR4: `BookingPricingService.calculate_price(room_price, nights)` returns a
  `Decimal` total: nightly price multiplied by nights. It combines information
  from Room and BookingDates without changing either. Negative, non-finite or
  non-numeric rates and non-positive/non-integer nights raise `ValueError`.
  A zero rate is allowed; no currency conversion, taxes or discounts are added.

Member 3 should create `BookingDates` from DTO dates, retrieve Room, calculate
the price using `room.nightly_price` and `dates.nights`, then pass dates and
total price to Booking. Member 4's handler should retrieve Room using the
event's room ID and call `room.reserve(event.booking_id, event.dates)`.
Overlap enforcement stays in Room. The handler/application must report its
rejection rather than editing reservations directly.

No Factory is needed: ordinary constructors are sufficient for this small
model. No Layer Supertype is used: there is no shared domain behaviour that
justifies a common base class. Domain components import only the standard
library and other domain components.

## Current tests and evidence

| Test | Behaviour |
| --- | --- |
| T1 / BR1 | Reject equal/reversed dates; accept a one-night stay; value equality and immutability. |
| T2 / BR2 | Valid state changes; reject changes from terminal states; confirmation event data. |
| T3 / BR3 | Reject five overlap shapes without mutation; accept adjacent stays; protect reservation records. |
| T4 / BR4 | Exact rate-times-nights calculation; reject invalid calculation inputs. |

T1 and T3 provide rejection cases, and T1 covers the equal-date and one-night
boundaries. There is one test function per implemented identifier, without
parameterization multiplying the coursework's intended eight tests.

The application, infrastructure, interface and T5-T8 remain placeholders.
The event handler and complete workflow have not been implemented or tested.
`evidence/member2-tests.txt` contains the actual T1-T4 run. This is not yet
a complete eight-test coursework submission.

For Member 2's TDD example, T1 was run against an immutable BookingDates
dataclass that had no validation. It failed because equal dates were accepted.
Adding BR1 validation and the nights property made that same test pass:

- `evidence/member2-red.txt`: `py -m pytest tests/test_br1.py -q` before BR1 implementation.
- `evidence/member2-green.txt`: the same command after BR1 implementation.

These are actual outputs suitable for the BR1 TDD example on Slide 12.

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
contract and dependency setup, and helped implement Member 2's domain
components, T1-T4, TDD evidence and documentation.

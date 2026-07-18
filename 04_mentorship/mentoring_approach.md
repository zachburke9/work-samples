# How I Mentor

Mentoring a junior analyst is not about transferring facts. Facts are cheap and
searchable. It is about building judgment and habits, so the person needs me
less on the next problem, not more. The measure of good mentoring is not how
much the mentee leans on me. It is how quickly they stop having to.

None of what follows depends on any particular tool. These are the habits I
coach, and the kind of moment where each one tends to come up.

## Teach the question before the query

The most common mistake is not bad SQL. It is a precise answer to the wrong
question. When someone brings me a request, the first thing I ask is what
decision the number is for. "Bookings by region" means one thing to a pricing
conversation and another to a staffing one. I would rather spend ten minutes on
the question than an hour on a clean answer nobody needed.

Example: an analyst was asked for "cancellations last month" and wrote a correct
query filtered on the cancellation date. The requester actually wanted
cancellations of bookings that were made last month, a different grain entirely.
We caught it by asking who would read it and why. Asking first is worth more
than any syntax.

## Validate before you trust

Before a dataset feeds anything, check it: missing values, duplicate keys,
impossible numbers. The first few times, I have the mentee run those checks out
loud, so it becomes reflex rather than a step they skip when they are busy. A
number that looks right and is wrong does more damage than an obvious error,
because no one thinks to question it.

Example: a report looked fine until we noticed the row count had quietly halved
after a join. One key had duplicates, and the join was dropping matches. Now the
habit is automatic: check the shape before you trust the total.

## Decide the grain before you write

"One row per what?" is the question I ask most. One row per booking, per night,
per customer, per day: each is a different query and a different answer. An
analyst who names the grain out loud before writing almost never produces the
double-counted total that takes an afternoon to debug later.

## Name it for the reader

A column called `flg_actv_1` will stall a meeting the moment someone asks what
it means. I coach analysts to name every output for the state the reader cares
about, not the database encoding: `is_active`, `Booked`, `Stayed`. The last mile
of an analysis is making it legible, and that is part of the work, not an
afterthought someone else cleans up.

## Lead with the answer

When an analyst reports back, the instinct is to narrate the journey: the
tables, the joins, the caveats, and finally the number. I coach the reverse.
Lead with the answer and the one or two figures that carry it, then offer the
supporting detail for anyone who wants it. A leader has to digest it in seconds
and relay it onward. Respecting that is a skill, and it is learnable.

## Understand it before you change it

When someone inherits a query that looks wrong, the reflex is to fix it. I slow
that down. Odd-looking logic is load-bearing more often than it is a mistake, so
the rule is: figure out why it is there before you touch it. If it turns out to
be genuinely wrong, change it openly and say what changed and why. If it was
right, you just learned something the original author knew. Either way you are
better off than you were guessing.

## Let them own something end to end

Confidence is built by finishing, not by watching me finish. As soon as someone
is ready, I hand off a real deliverable, start to end, and stay available
without hovering. Reviewing their work is teaching, not gatekeeping: I point at
the specific thing and the reason, never just "change this." And I make it safe
to say "I do not know yet," because an analyst who can admit the edge of their
knowledge is far safer than one who guesses to look sure.

## The throughline

Every habit above is really the same lesson in a different place: understand the
real need, check your work, make it legible, and be honest about what you know.
Tools change. Those do not. If a mentee leaves with those habits, they will be a
good analyst in any stack, working with any tools, long after they have
forgotten who taught them.

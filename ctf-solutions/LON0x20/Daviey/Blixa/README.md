Blixa
=====

This is a "Crypto" type challenge, where the premise is that a lottery draw of
6 numbers (between 0 and 255) is drawn every minute, hence the fancy banner of
"Minute Lotto".

The source code for the server component is provided and it is golang.  There
is a public service running on `c.ctf.turtleturtleup.com:1339`.

Reading the source code we can see that if we match the correct 6 numbers, then
then flag is returned which is stored as an environmental variable as "FLAG".
Therefore, we know that local exploitation will not be possible as the FLAG
isn't related to the source and is dependant on the remote environment.

On the imports, we can see ["math/rand"](https://golang.org/pkg/math/rand/) which is well known for producing
pseudo-random rather than the library ["crypto/rand"](https://golang.org/pkg/crypto/rand/) which produces
cryptographically secure randomisation.  Infact, the description for the
"math/rand" package states "use a default shared Source that produces a
deterministic sequence of values each time a program is run"

Therefore, we can expect to look for some issue with the random selection.

Understanding the seed
----------------------

On Line 21 of the server code, we see:
`var globalSeed = rand.New(rand.NewSource(time.Now().UnixNano())).Int63n(999999)`

Working from the inside out, we see that the parameter of
`time.Now().UnixNano()`, which is the current Unix time (epoch time) in
nanoseconds, or the number of nanoseconds elapsed since January 1, 1970 UTC.

An example of this is: 1257894000000000000, which is 2009-11-10 23:00:00 +0000
UTC.

Then `rand.NewSource()` produces a pseudo-random Source, seeded with a value
derived from the current time in nanoseconds.  This Source is then used to
return an Int63n, which is a non-negative pseudo-random number, with the
maximum value being 999999.  Therefore, we know that the globalSeed will be
between 1 and 999999.

To confirm that this is the weakness, we can hard-code the globalSeed and run
the server component and we should see a consistent stream of draw results.
However, we don't. :(

Understanding each draw
-----------------------

Now we have a consistent seed, we can see that each draw isn't fully dependant
on this source alone.

On Line 118 of the server code, we see:
`r := rand.New(rand.NewSource(globalSeed + time.Now().Truncate(time.Minute).Unix()))`

This adds the current time, which is truncated to the nearest minute (drops the
seconds) and represented in Unix time.  This means that each run the
deterministic random number is derived from `globalSeed + CurrentTime`, which
increments each time there is a draw by 60 seconds.

If we hard-code the current time in addition to the globalSeed, we can now see
that each time the tool is run a deterministic series of draws is returned.

Reversing the results to find the seed
--------------------------------------

We know that a deterministic stream is created by:

`globalSeed + CurrentTime = Results`

We know the draw results, as they are returned by the server every minute.  We
also know the current time by checking our local time.

The truncation of the current time to the nearest minute makes it much easier
to be able to reverse the results.  This is because it would be very difficult
to be sure of the server time to the nearest second, but we can be pretty
confident out local machine and the server are running to the same minute.

Therefore, if we take the CurrentTime and enumerate over every possible
globalSeed, using the same formula we should be able to intercept the draw
results.  This will confirm the servers globalSeed.

We can see this implemented in the getCurrentSeed() function in the attached
code.

Predicting the future
---------------------

Now we are able to determine the server's globalSeed, we are able to produce
the draw results in paraell to the server.  However, this doesn't help us work
out what the next results will be.

However, due to the time truncation to the nearest minute we know that adding
60, 120 & 180 to the CurrentTime will return to us the next 3 draw results
without having to wait.

This is implemented in the predictNext() code in the attached code.

Interesting Caveat
------------------

The [Go Playground](https://play.golang.org) is an excellent resource for experimental go code.  However,
the Go Playground is a fully deterministic environment which means that the
current time is a constant of "2009-11-10 23:00:00 UTC" which is Go's birthday.
This means that the client code needs to be run locally.

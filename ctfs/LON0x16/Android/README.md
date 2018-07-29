# SecTalksLON0x16

By imh0tep

A simple Android app containing three flags to provide an intro to reversing Android applications.

The build APK can be found in the root directory and the project can be opened in Android Studio.

NDK is used to obfuscate strings but is not intentended to be a target.

## Flag 1

Simple string defined in `strings.xml`.  Running `strings` against the extracted APK (specifically `resources.arsc` should be enough to find it).

## Flag 2

A flag is written to the private (sandboxed) file system of the app.  While a rooted phone could be used to browse to this directory, root is not required to retrieve the flag.  Performing an adb backup of the application will allow extract the app's sandboxe filesystem and allow exploration.

## Flag 3

An http request is sent to a server (a simple Flask server, included in the root directory as `server.py`) with some headers.  If Burp Proxy or similar is used, inspection should show that a header, `X-Admin: False` is being sent.  Manipulation of this to change it to `X-Admin: True` will cause the flag to be sent back in an `X-Flag` header.  The server also restricts requests to User-Agents containing the string `Android` to deter `curl`ing from a non-mobile platform.

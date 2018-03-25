# The sixth one

In this one the flag is encoded as bits.  Since ASCII only requires up to 7 bits, each character is encoded with only 7 bits (to add to the confusion when naively printing the decoded result).  Each bit is encoded either as the color `0xaa38ff` or `0xb55b97`, in a 7x7 pixel block (the number 7 being important here).
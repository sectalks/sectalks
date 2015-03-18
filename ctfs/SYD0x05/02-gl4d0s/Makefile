# gl4d0s: A single-purpose cr0n job designed to be broken.
# Copyright (C) 2015 Aleksa Sarai <cyphar@cyphar.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# 1. The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

SRC = $(wildcard *.go)
OUT = gl4d0s

LOG_DIR = /var/log/gl4d0s/
RUN_DIR = /var/run/gl4d0s/

SUSER  ?= root
SGROUP ?= root
LUSER  ?= gl4dl0gs
LGROUP ?= gl4dl0gs

.PHONY: all clean

all: $(OUT)

clean:
	@echo " [CLEAN]   ."
	@rm -f $(OUT)

$(OUT): $(SRC)
	@echo " [GO]      $<"
	@go build -o $@

install: $(OUT)
	@echo " [INSTALL] $(OUT)"
	@cp $(OUT) /usr/bin/$(OUT)
	@echo " [PERM]    $(OUT)"
	@chown $(SUSER):$(SGROUP) /usr/bin/$(OUT)
	@#chmod ug+s /usr/bin/$(OUT) # This isn't actually needed -- we're using cr0n.
	@echo " [MKDIR]   $(LOG_DIR)"
	@mkdir -p "$(LOG_DIR)"
	@chown $(LUSER):$(LGROUP) $(LOG_DIR)
	@echo " [MKDIR]   $(RUN_DIR)"
	@mkdir -p "$(RUN_DIR)"
	@chown $(LUSER):$(LGROUP) $(RUN_DIR)

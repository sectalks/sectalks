FROM node:14-alpine

# RUN npm install -g uglify-js 
RUN npm install -g @node-minify/cli @node-minify/babel-minify

RUN npm install static-server chalk crypto-js

WORKDIR /workdir
COPY . .
RUN mkdir -p /workdir/html/flag

ENV FLAG="testflag"
ENV SECRET="Search here....."

RUN cp src/hard.js /tmp/hard.js
# document
RUN sed -i 's/window.document/window[decode(31)]/g' /tmp/hard.js && \
    sed -i 's/window.CryptoJS/window[decode(38)]/g' /tmp/hard.js && \
    sed -i 's/window.JSON/window[decode(44)]/g' /tmp/hard.js
# string constant
RUN sed -i 's/"log"/decode(1)/g' /tmp/hard.js && \
    sed -i 's/"GET"/decode(3)/g' /tmp/hard.js && \
    sed -i 's/"12so9bd6kd3d"/decode(4)/g' /tmp/hard.js && \
    sed -i 's/"alert"/decode(16)/g' /tmp/hard.js && \
    sed -i 's/"console"/decode(7)/g' /tmp/hard.js && \
    sed -i 's/"sectalks{"/decode(8)/g' /tmp/hard.js && \
    sed -i 's/"date-in"/decode(10)/g' /tmp/hard.js && \
    sed -i 's/"}"/decode(9)/g' /tmp/hard.js && \
    sed -i 's/"0fg5ku1skd0k"/decode(14)/g' /tmp/hard.js &&\
    sed -i 's/"search-input"/decode(20)/g' /tmp/hard.js && \
    sed -i 's/"\/flag\/sectalks"/decode(19)/g' /tmp/hard.js && \
    sed -i 's/"Check Availability"/decode(21)/g' /tmp/hard.js && \
    sed -i 's/"click"/decode(23)/g' /tmp/hard.js && \
    sed -i 's/"button"/decode(24)/g' /tmp/hard.js && \
    sed -i 's/"textContent"/decode(27)/g' /tmp/hard.js && \
    sed -i 's/"%c"/decode(28)/g' /tmp/hard.js && \
    sed -i 's/"XMLHttpRequest"/decode(32)/g' /tmp/hard.js &&\
    sed -i 's/"Date"/decode(37)/g' /tmp/hard.js && \
    sed -i 's/""/decode(55)/g' /tmp/hard.js && \
    sed -i 's/"az"/decode(57)/g' /tmp/hard.js
# .fn()
RUN sed -i 's/\.toString(/[decode(0)](/g' /tmp/hard.js && \
    sed -i 's/\.console(/[decode(7)](/g' /tmp/hard.js && \
    sed -i 's/\.get(/[decode(18)](/g' /tmp/hard.js && \
    sed -i 's/\.getElementsByTagName(/[decode(22)](/g' /tmp/hard.js && \
    sed -i 's/\.addEventListener(/[decode(25)](/g' /tmp/hard.js && \
    sed -i 's/\.pop(/[decode(26)](/g' /tmp/hard.js && \
    sed -i 's/\.getElementById(/[decode(29)](/g' /tmp/hard.js && \
    sed -i 's/\.decrypt(/[decode(30)](/g' /tmp/hard.js && \
    sed -i 's/\.preventDefault(/[decode(33)](/g' /tmp/hard.js && \
    sed -i 's/\.stopPropagation(/[decode(34)](/g' /tmp/hard.js && \
    sed -i 's/\.setInterval(/[decode(35)](/g' /tmp/hard.js && \
    sed -i 's/\.getTime(/[decode(36)](/g' /tmp/hard.js && \
    sed -i 's/\.substring(/[decode(39)](/g' /tmp/hard.js && \
    sed -i 's/\.open(/[decode(40)](/g' /tmp/hard.js && \
    sed -i 's/\.send(/[decode(42)](/g' /tmp/hard.js && \
    sed -i 's/\.stringify(/[decode(45)](/g' /tmp/hard.js && \
    sed -i 's/\.charCodeAt(/[decode(56)](/g' /tmp/hard.js
# .obj[
RUN sed -i 's/\.AES\[/[decode(52)][/g' /tmp/hard.js
# .obj.
RUN sed -i 's/\.enc\./[decode(53)]./g' /tmp/hard.js
# .property =
RUN sed -i 's/\.onreadystatechange  *=/[decode(41)] =/g' /tmp/hard.js && \
    sed -i 's/\.readyState  *=/[decode(43)] =/g' /tmp/hard.js
# .property; / .propertyEOL
RUN sed -i 's/\.response *;/[decode(46)];/g' /tmp/hard.js && \
    sed -i 's/\.response *$/[decode(46)]/g' /tmp/hard.js && \
    sed -i 's/\.value *;/[decode(47)];/g' /tmp/hard.js && \
    sed -i 's/\.value *$/[decode(47)]/g' /tmp/hard.js && \
    sed -i 's/\.selectedIndex *;/[decode(48)];/g' /tmp/hard.js && \
    sed -i 's/\.selectedIndex *$/[decode(48)]/g' /tmp/hard.js && \
    sed -i 's/\.elements *;/[decode(49)];/g' /tmp/hard.js && \
    sed -i 's/\.elements *$/[decode(49)]/g' /tmp/hard.js && \
    sed -i 's/\.forms *;/[decode(50)];/g' /tmp/hard.js && \
    sed -i 's/\.forms *$/[decode(50)]/g' /tmp/hard.js && \
    sed -i 's/\.placeholder *;/[decode(51)];/g' /tmp/hard.js && \
    sed -i 's/\.placeholder *$/[decode(51)]/g' /tmp/hard.js
# .property)
RUN sed -i 's/\.Utf8 *)/[decode(54)])/g' /tmp/hard.js
# .property | / .property &
RUN sed -i 's/\.response  */[decode(46)] /g' /tmp/hard.js && \
    sed -i 's/\.value  */[decode(47)] /g' /tmp/hard.js && \
    sed -i 's/\.selectedIndex  */[decode(48)] /g' /tmp/hard.js && \
    sed -i 's/\.elements  */[decode(49)] /g' /tmp/hard.js && \
    sed -i 's/\.forms  */[decode(50)] /g' /tmp/hard.js && \
    sed -i 's/\.placeholder  */[decode(51)] /g' /tmp/hard.js

# Debug
# RUN sed -i 's/\/\/DEBUG:\ //g' /tmp/hard.js
RUN sed -i 's/\/\/DEBUG_LOG:\ //g' /tmp/hard.js
RUN sed -i 's/\/\/DEBUG_CONSOLE:\ //g' /tmp/hard.js

RUN cat /tmp/hard.js
# RUN /usr/local/bin/uglifyjs --mangle --toplevel --output ./html/js/hard.js -- /tmp/hard.js
RUN /usr/local/bin/node-minify --compressor babel-minify --output ./html/js/hard.js --input /tmp/hard.js
# RUN cp /tmp/hard.js ./html/js/hard.js
RUN sed -i 's/\/\/.*$//g' ./html/js/hard.js

CMD ["node", "index.js"]
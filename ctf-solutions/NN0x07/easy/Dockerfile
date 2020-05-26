FROM node:14-alpine

RUN npm install -g uglify-js 

RUN npm install static-server chalk crypto-js

WORKDIR /workdir
COPY . .
RUN mkdir -p /workdir/html/flag

ENV FLAG="testflag"

RUN cp src/easy.js /tmp/easy.js
# document
RUN sed -i 's/window.document/window[decode(31)]/g' /tmp/easy.js && \
    sed -i 's/window.JSON/window[decode(44)]/g' /tmp/easy.js
# string constant
RUN sed -i 's/"log"/decode(1)/g' /tmp/easy.js && \
    sed -i 's/"GET"/decode(3)/g' /tmp/easy.js && \
    sed -i 's/"input"/decode(4)/g' /tmp/easy.js && \
    sed -i 's/"h2"/decode(20)/g' /tmp/easy.js && \
    sed -i 's/"console"/decode(7)/g' /tmp/easy.js && \
    sed -i 's/"sectalks{"/decode(8)/g' /tmp/easy.js && \
#     sed -i 's/"date-in"/decode(9)/g' /tmp/easy.js && \
    sed -i 's/"}"/decode(10)/g' /tmp/easy.js && \
    sed -i 's/"\/flag\/"/decode(12)/g' /tmp/easy.js &&\
#     sed -i 's/"search-input"/decode(16)/g' /tmp/easy.js && \
    sed -i 's/"\/flag\/submit"/decode(19)/g' /tmp/easy.js && \
    sed -i 's/"keyup"/decode(21)/g' /tmp/easy.js && \
    sed -i 's/"click"/decode(23)/g' /tmp/easy.js && \
    sed -i 's/"button"/decode(24)/g' /tmp/easy.js && \
    sed -i 's/"textContent"/decode(27)/g' /tmp/easy.js && \
#     sed -i 's/"%c"/decode(28)/g' /tmp/easy.js && \
    sed -i 's/"XMLHttpRequest"/decode(32)/g' /tmp/easy.js &&\
    sed -i 's/"could_it_be"/decode(37)/g' /tmp/easy.js && \
    sed -i 's/"Park Hyatt"/decode(55)/g' /tmp/easy.js && \
    sed -i 's/""/decode(38)/g' /tmp/easy.js
# .fn()
RUN sed -i 's/\.toString(/[decode(0)](/g' /tmp/easy.js && \
#     sed -i 's/\.console(/[decode(7)](/g' /tmp/easy.js && \
#     sed -i 's/\.get(/[decode(18)](/g' /tmp/easy.js && \
    sed -i 's/\.getElementsByTagName(/[decode(22)](/g' /tmp/easy.js && \
    sed -i 's/\.addEventListener(/[decode(25)](/g' /tmp/easy.js && \
    sed -i 's/\.toLowerCase(/[decode(52)](/g' /tmp/easy.js && \
#     sed -i 's/\.getElementById(/[decode(29)](/g' /tmp/easy.js && \
    sed -i 's/\.preventDefault(/[decode(33)](/g' /tmp/easy.js && \
    sed -i 's/\.stopPropagation(/[decode(34)](/g' /tmp/easy.js && \
    sed -i 's/\.substring(/[decode(39)](/g' /tmp/easy.js && \
    sed -i 's/\.open(/[decode(40)](/g' /tmp/easy.js && \
    sed -i 's/\.send(/[decode(42)](/g' /tmp/easy.js && \
    sed -i 's/\.stringify(/[decode(45)](/g' /tmp/easy.js
# .obj[
# RUN sed -i 's/\.AES\[/[decode(52)][/g' /tmp/easy.js
# .obj.
# RUN sed -i 's/\.enc\./[decode(53)]./g' /tmp/easy.js
# .property =
RUN sed -i 's/\.onreadystatechange  *=/[decode(41)] =/g' /tmp/easy.js && \
    sed -i 's/\.readyState  *=/[decode(43)] =/g' /tmp/easy.js
# .property; / .propertyEOL
RUN sed -i 's/\.response *;/[decode(46)];/g' /tmp/easy.js && \
    sed -i 's/\.response *$/[decode(46)]/g' /tmp/easy.js && \
    sed -i 's/\.value *;/[decode(47)];/g' /tmp/easy.js && \
    sed -i 's/\.value *$/[decode(47)]/g' /tmp/easy.js && \
    sed -i 's/\.selectedIndex *;/[decode(48)];/g' /tmp/easy.js && \
    sed -i 's/\.selectedIndex *$/[decode(48)]/g' /tmp/easy.js && \
    sed -i 's/\.elements *;/[decode(49)];/g' /tmp/easy.js && \
    sed -i 's/\.elements *$/[decode(49)]/g' /tmp/easy.js && \
    sed -i 's/\.forms *;/[decode(50)];/g' /tmp/easy.js && \
    sed -i 's/\.forms *$/[decode(50)]/g' /tmp/easy.js
# .property)
RUN sed -i 's/\.textContent *)/[decode(27)])/g' /tmp/easy.js
# .property | / .property &
RUN sed -i 's/\.response  */[decode(46)] /g' /tmp/easy.js && \
    sed -i 's/\.value  */[decode(47)] /g' /tmp/easy.js && \
    sed -i 's/\.selectedIndex  */[decode(48)] /g' /tmp/easy.js && \
    sed -i 's/\.elements  */[decode(49)] /g' /tmp/easy.js && \
    sed -i 's/\.forms  */[decode(50)] /g' /tmp/easy.js

RUN cat /tmp/easy.js
RUN /usr/local/bin/uglifyjs --mangle --toplevel --output ./html/js/easy.js -- /tmp/easy.js
#RUN /usr/local/bin/node-minify --compressor google-closure-compiler --output ./html/js/easy.js --input /tmp/easy.js --option '{"compilationLevel": "WHITESPACE_ONLY", "warningLevel": "VERBOSE"}'
#RUN /usr/local/bin/node-minify --compressor babel-minify --output ./html/js/easy.js --input /tmp/easy.js


CMD ["node", "index.js"]
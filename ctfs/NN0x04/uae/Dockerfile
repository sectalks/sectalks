FROM tomcat:9.0.21-jdk8

ENV JYTHON_VERSION="2.7.1" \
    JYTHON_SHASUM="392119a4c89fa1b234225d83775e38dbd149989f"

RUN curl -fSL -o jython_installer.jar "http://search.maven.org/remotecontent?filepath=org/python/jython-installer/${JYTHON_VERSION}/jython-installer-${JYTHON_VERSION}.jar" \
 && echo "$JYTHON_SHASUM *jython_installer.jar" | sha1sum -c - \
 && java -jar jython_installer.jar -s -d /usr/local/jython \
 && rm jython_installer.jar \
 && ln -s /usr/local/jython/bin/jython /usr/local/jython/bin/python \
 && ln -s /usr/local/jython/bin/jython /usr/local/jython/bin/python2

ENV PATH="/usr/local/jython/bin:$PATH"

# separating this makes incremental building fast
COPY src/requirements.txt /
RUN pip install -r /requirements.txt

RUN mkdir /chal

COPY src /chal/uae

RUN tar czvf /code.tgz /chal/uae

RUN javac /chal/uae/java/com/adamyi/uae/*.java

RUN mkdir /chal/uae/WEB-INF/lib \
 && cp /usr/local/jython/jython.jar /chal/uae/WEB-INF/lib

WORKDIR /chal/uae

RUN rm -rf /usr/local/tomcat/webapps/*
COPY tomcat/ROOT.xml /usr/local/tomcat/conf/Catalina/localhost/ROOT.xml
COPY tomcat/server.xml /usr/local/tomcat/conf/server.xml
COPY tomcat/keystore.jks /keystore.jks

ENV JYTHONPATH "/chal/uae/java"

COPY run.sh /run.sh
COPY init.py /init.py
CMD /run.sh

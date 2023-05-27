FROM node:19-alpine

RUN mkdir -p /usr/src/
WORKDIR /usr/src/
COPY package.json .
RUN npm install

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app
COPY . .
RUN chown -R root:root /usr/src/app/*
RUN chmod -R 755 /usr/src/app/*

USER node
CMD [ "node", "server.js" ]

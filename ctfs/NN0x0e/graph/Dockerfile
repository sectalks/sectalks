FROM node:18-alpine3.15

RUN adduser -S -s /bin/false -H -D user

ENV NODE_ENV production

WORKDIR /app

COPY ./docker-files/package*.json /app/

RUN npm ci --only=production 

COPY ./docker-files/ /app

CMD ["node", "server.js"]

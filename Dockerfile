FROM node:10.8.0-alpine

COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock

WORKDIR /app

RUN npm install -g yarn

# install everything

RUN NODE_ENV=development yarn install

COPY . /app

ARG API_URL
ARG SENTRY_PUBLIC_DSN
ARG NODE_ENV
ARG PIWIK_URL
ARG PIWIK_SITE_ID

# for javascript browser build
ENV API_URL=$API_URL
ENV SENTRY_PUBLIC_DSN=$SENTRY_PUBLIC_DSN
ENV NODE_ENV=$NODE_ENV
ENV PIWIK_URL=$PIWIK_URL
ENV PIWIK_SITE_ID=$PIWIK_SITE_ID

RUN npm run build

ENTRYPOINT ["npm", "start"]

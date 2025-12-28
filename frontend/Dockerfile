FROM node:22-alpine as build

ARG REACT_APP_DD_APP_ID
ARG REACT_APP_DD_CLIENT_TOKEN
ARG REACT_APP_DD_ENV=local

ENV REACT_APP_DD_APP_ID=$REACT_APP_DD_APP_ID
ENV REACT_APP_DD_CLIENT_TOKEN=$REACT_APP_DD_CLIENT_TOKEN
ENV REACT_APP_DD_ENV=$REACT_APP_DD_ENV

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm install

COPY public ./public
COPY src ./src

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

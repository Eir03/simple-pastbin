FROM node:16-alpine as builder

WORKDIR /app

COPY package.json package-lock.json /app/

RUN npm install

COPY . /app


RUN npm run build

FROM nginx:1.23-alpine

COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
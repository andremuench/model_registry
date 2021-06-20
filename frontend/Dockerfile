ARG BUILDER_IMAGE
FROM ${BUILDER_IMAGE} AS builder
COPY my-app /app

WORKDIR /app
RUN npm ci
RUN npm run build

# Build server
FROM nginx:1.17.8

COPY default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build /var/www

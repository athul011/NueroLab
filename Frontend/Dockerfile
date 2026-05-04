



FROM node:20.13-alpine AS builder

WORKDIR /app


RUN apk add --no-cache --virtual .build-deps \
    python3 \
    make \
    g++


COPY package.json package-lock.json ./


RUN npm ci --frozen-lockfile


COPY . .


RUN npm run build


FROM node:20.13-alpine

WORKDIR /app


RUN apk add --no-install-recommends --no-cache \
    dumb-init


RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser


COPY --from=builder --chown=appuser:appuser /app/.next ./.next
COPY --from=builder --chown=appuser:appuser /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appuser /app/package.json ./


USER appuser


EXPOSE 3000


HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})"


ENTRYPOINT ["/usr/sbin/dumb-init", "--"]


CMD ["npm", "start"]

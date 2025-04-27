# FROM node:20-slim AS builder
FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# Production image
# FROM node:20-slim
FROM node:20-alpine

WORKDIR /app
RUN npm install -g serve

# Copy built files only
COPY --from=builder /app/dist /app/dist

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]

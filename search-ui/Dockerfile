FROM node:20-slim AS builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# Production image
FROM node:20-slim

WORKDIR /app
RUN npm install -g serve

# Copy built files only
COPY --from=builder /app/dist /app/dist

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]

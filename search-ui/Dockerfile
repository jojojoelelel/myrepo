# Builder image
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .
RUN npm run build

FROM node:20-alpine 

# Set working directory
WORKDIR /app

# Install serve
RUN npm install -g serve

# Copy built files only
COPY --from=builder /app/dist /app/dist

# Expose port 3000
EXPOSE 3000

# Run serve
CMD ["serve", "-s", "dist", "-l", "3000"]

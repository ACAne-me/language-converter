# Stage 1: Build the Next.js application
FROM node:18-alpine AS builder
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve the application with a lightweight web server
FROM node:18-alpine AS runner
WORKDIR /app

# Copy built files and node_modules from builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

# Set environment variables
ENV NODE_ENV=production
ENV NEXT_PUBLIC_API_URL=http://backend:8000

# Expose port 3000
EXPOSE 3000

# Start the Next.js application
CMD ["npm", "start"]
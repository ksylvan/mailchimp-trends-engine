# Stage 1: Builder
FROM node:23-alpine AS builder
WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy package.json and pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy the rest of the application source code
COPY . .

# Build the Next.js application
RUN pnpm build

# Stage 2: Runner
FROM node:23-alpine AS runner
WORKDIR /app

# Set environment variables
ENV NODE_ENV=production
# Optionally, set NEXT_TELEMETRY_DISABLED to 1 to disable telemetry
# ENV NEXT_TELEMETRY_DISABLED 1

# Copy built assets from the builder stage
# The standalone output copies server files and static assets.
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

# Expose port 3000
EXPOSE 3000

# Command to run the Next.js application
# The server.js file is part of the standalone output.
CMD ["node", "server.js"]

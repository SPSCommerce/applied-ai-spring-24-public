# Use an official Node runtime as a parent image
FROM node:20.0-slim

# Set the working directory in the container
WORKDIR /app

# Copy package.json and yarn.lock files
COPY ./package.json ./yarn.lock /app/

# Install dependencies using Yarn
RUN yarn install

# Bundle
COPY . /app

# Build
RUN yarn build

# Make VITE port 5173 available to the world outside this container
EXPOSE 5173

# Run Dev Server
CMD ["yarn", "dev", "--host", "0.0.0.0", "--port", "5173"]


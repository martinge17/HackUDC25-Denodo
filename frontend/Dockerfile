FROM node:18-alpine

# Set workdir inside container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install deps
RUN npm install

# Copy the remaining of files
COPY . .

# Run the APP (DEVELOPMENT ONLY)
CMD ["npm","start"]

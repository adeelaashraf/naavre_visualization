# Use a base image with Node.js installed
FROM node:14-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Copy vite.config.js to the container
COPY vite.config.js ./

# Install project dependencies
RUN npm install

# Copy the rest of the project files to the container
COPY favicon.ico /app
COPY main.js /app
COPY index.html /app
COPY style.css /app

COPY data.json /app
COPY version.json /app

# Expose the port your application will run on (if needed)
EXPOSE 5173

# Start the application and echo the IP address link
CMD npm start && sh -c "ip route show default | awk '/default/ {print \"Application running at http://\" $3 \":5173\"}'"


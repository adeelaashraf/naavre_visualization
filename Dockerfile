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

COPY python_scripts /app/python_scripts
COPY configs /app/configs

# Install Python 3 and pip
RUN apk add --no-cache python3 py3-pip

# Optionally, upgrade pip
RUN pip3 install --upgrade pip

# Install Rasterio
RUN apk add --no-cache \
    build-base \
    python3-dev \
    geos-dev \
    proj-dev \
    gdal-dev \
    && pip3 install rasterio

RUN pip3 install --no-cache-dir -r python_scripts/requirements.txt

# Copy the entrypoint script into the container
COPY entrypoint_time.sh /app/entrypoint_time.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint_time.sh

# Expose the port your application will run on (if needed)
EXPOSE 5173

# Set the entrypoint script as the entrypoint for the container
ENTRYPOINT ["/app/entrypoint_time.sh"]

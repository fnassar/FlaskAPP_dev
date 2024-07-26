FROM --platform=linux/amd64 python:3.12-slim

# Optional: for development mode
ENV FLASK_ENV=development  

# Set the working directory
WORKDIR /app

# Copy all the application files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the ports the apps run on
EXPOSE 5000 5001 5002 5003 5004 5005 5006

# Copy the startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Run the startup script
CMD ["/start.sh"]

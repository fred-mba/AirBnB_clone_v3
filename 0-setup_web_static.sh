#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

# Step:1 => Install Nginx if it not already installed
if ! command -v nginx;
then
    echo "Nginx is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install nginx -y
    sudo systemctl start nginx.service

    # Ensuring nginx can be managed via init
    sudo systemctl enable nginx

else
    echo "Nginx is already installed. Skipping installation."
fi

# Create necessary parent directories
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# Adjust the permissions or ownership of the folders
sudo chown -R ubuntu:ubuntu /data/
sudo chmod -R 755 /data/

# Step 2: => create sample pages
echo "Holberton School" > /data/web_static/releases/test/index.html

# Step 3: => Creating Server Block Files
sudo sed -i '49i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# Step 4: => Creating symbolic links
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/web_static/current

# sudo ln -s "/etc/nginx/sites-available/default" "/etc/nginx/sites-enabled/"
echo "Symbolic link created successfully."

# If no problems were found, restart Nginx to enable your changes
sudo nginx -t
sudo systemctl restart nginx

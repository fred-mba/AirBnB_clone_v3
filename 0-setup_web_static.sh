#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

# Step:1 => Install Nginx if it not already installed
if ! command -v nginx &> /dev/null;
then
    echo "Nginx is not installed. Installing..."
    apt-get update -y
    apt-get install nginx -y
    systemctl start nginx.service

    # Ensuring nginx can be managed via init
    systemctl enable nginx

else
    echo "Nginx is already installed. Skipping installation."
fi

# Create necessary parent directories
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# Adjust the permissions or ownership of the folders
chown -R ubuntu:ubuntu /data
chmod -R 755 /data

# Step 2: => create sample pages
tee /data/web_static/releases/test/index.html <<EOF
<html>
    <head>
    </head>
    <body>
      Holberton School
    </body>
</html>
EOF

# Step 3: => Creating Server Block Files
tee /etc/nginx/sites-available/myconfig.config <<EOF
server {
        listen 80;

        server_name _;

        location /hbnb_static/ {
                alias /data/web_static/current/;
        }
}
EOF

# Step 4: => Creating symbolic links
original_path="/data/web_static/releases/test/"
link_path="/data/web_static/current"

if [ -L "$link_path" ]; then
    echo "Symbolic link already exist. Deleting..."
    rm "$link_path"
else
    ln -s "$original_path" "$link_path"
    echo "Symbolic link created successfully."
fi

# Test the configuration files
# If no problems were found, restart Nginx to enable your changes
test_nginx="nginx -t"
if [ "$test_nginx" ]; then
    echo "Nginx configuration test successfull. Restarting now..."
    systemctl restart nginx
else
    echo "Nginx configuration failed. Skipping restart!"
fi

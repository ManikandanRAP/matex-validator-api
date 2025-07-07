# Production Deployment Guide: MatEx RAP Validator API

This guide provides step-by-step instructions to deploy the FastAPI application to a production environment on a Linux server (Ubuntu). This setup uses **Gunicorn** to manage the application, **Systemd** to run it as a background service, and **Nginx** as a secure reverse proxy.

---

### **Prerequisites**

- A Linux server (Ubuntu 20.04 or newer).
- A domain name pointing to your server's public IP address (required for HTTPS).
- You have connected to your server via SSH.

--- 

### **Step 1: Initial Server Setup**

First, update your server's packages and install the necessary tools.

```bash
# Update package lists and upgrade
sudo apt update && sudo apt upgrade -y

# Install Python, Pip, Venv, Nginx, and Git
sudo apt install python3-pip python3-dev python3-venv nginx git -y
```

### **Step 2: Clone Project and Set Up Environment**

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/ManikandanRAP/matex-validator-api.git
    cd matex-validator-api
    ```

2.  **Create a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    Install Gunicorn alongside your other application dependencies.
    ```bash
    pip install -r requirements.txt gunicorn
    ```

4.  **Create `.env` file**
    Store your production secrets here. **Do not commit this file to Git.**
    ```bash
    nano .env
    ```
    Add your production token:
    ```
    API_TOKEN=your_super_secret_production_token
    ```
    Press `Ctrl+X`, `Y`, and `Enter` to save.

### **Step 3: Create a Systemd Service File**

Systemd will manage the Gunicorn process, ensuring it runs in the background and restarts on failure or server reboot.

1.  **Create a service file:**
    ```bash
    sudo nano /etc/systemd/system/matex-api.service
    ```

2.  **Paste the following configuration.** Make sure to replace `your_user` with your actual username (e.g., `ubuntu`).
    ```ini
    [Unit]
    Description=Gunicorn instance to serve MatEx RAP Validator API
    After=network.target

    [Service]
    User=your_user
    Group=www-data
    WorkingDirectory=/home/your_user/matex-validator-api
    Environment="PATH=/home/your_user/matex-validator-api/venv/bin"
    ExecStart=/home/your_user/matex-validator-api/venv/bin/gunicorn --workers 3 --worker-class uvicorn.workers.UvicornWorker -b 127.0.0.1:8000 app.main:app

    [Install]
    WantedBy=multi-user.target
    ```

3.  **Start and Enable the Service:**
    ```bash
    # Start the service
    sudo systemctl start matex-api

    # Enable it to start on boot
    sudo systemctl enable matex-api

    # Check the status to ensure it's running without errors
    sudo systemctl status matex-api
    ```

### **Step 4: Configure Nginx as a Reverse Proxy**

Nginx will listen for public traffic and forward it to your Gunicorn service.

1.  **Create an Nginx configuration file:**
    ```bash
    sudo nano /etc/nginx/sites-available/matex-api
    ```

2.  **Paste the following server block.** The `server_name` is set to your server's public IP address.
    ```nginx
    server {
        listen 80;
        server_name 182.73.35.202;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

3.  **Enable the configuration by creating a symbolic link:**
    ```bash
    sudo ln -s /etc/nginx/sites-available/matex-api /etc/nginx/sites-enabled
    ```

4.  **Test and Restart Nginx:**
    ```bash
    # Test for syntax errors
    sudo nginx -t

    # Restart Nginx to apply changes
    sudo systemctl restart nginx
    ```

### **Step 5: Adjust Firewall and Finalize**

1.  **Allow Nginx traffic:**
    ```bash
    sudo ufw allow 'Nginx Full'
    sudo ufw delete allow 8000 # No longer need to expose port 8000
    ```

Your API is now live and accessible via your public IP address: `http://182.73.35.202`.

### **A Note on Security (HTTPS)**

This guide sets up your API with standard HTTP, which is unencrypted. For a true production environment that handles real client data, **using HTTPS is essential for security.**

To enable HTTPS, you need a domain name. Services like Let's Encrypt provide free SSL certificates but require a domain to validate ownership. Using an IP address directly is suitable for testing and development, but we strongly recommend acquiring a domain name before going live with client traffic.

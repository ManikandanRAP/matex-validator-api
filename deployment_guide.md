# MatEx RAP Validator API - Demo Deployment Guide

This guide provides step-by-step instructions to deploy the FastAPI application to a Linux server (e.g., Ubuntu) for a demonstration. Follow these steps after connecting to your server via SSH.

---

### **Step 1: Update System and Install Prerequisites**

First, update your server's package list and install Python, `pip`, and the necessary tools.

```bash
# Update package lists and upgrade existing packages
sudo apt update
sudo apt upgrade -y

# Install Python 3, pip, venv, and git
sudo apt install python3 python3-pip python3-venv git -y
```

### **Step 2: Clone Your Project**

Next, download the application code from your Git repository.

```bash
# Clone your repository (replace with your actual repo URL)
git clone https://your-git-repository-url.com/matex-validator.git

# Navigate into your project directory
cd matex-validator
```

*Note: If your repository is private, you may need to configure SSH keys for authentication.*

### **Step 3: Create and Configure the Environment File**

Create a `.env` file to securely store your API token.

```bash
# Create and open the .env file using the nano editor
nano .env
```

Add the following line to the file, then press `Ctrl+X`, `Y`, and `Enter` to save and exit.

```
API_TOKEN=secret-token-for-dev
```

### **Step 4: Set Up the Python Virtual Environment**

Use a virtual environment to isolate the application's dependencies.

```bash
# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

Your terminal prompt should now be prefixed with `(venv)`.

### **Step 5: Install Dependencies**

Install the required Python packages from your `requirements.txt` file.

```bash
# Install dependencies using pip
pip install -r requirements.txt
```

### **Step 6: Configure the Firewall**

Allow incoming traffic on the port your application will use (default is 8000).

```bash
# Allow traffic on port 8000
sudo ufw allow 8000

# Enable the firewall if it's not already active
sudo ufw enable
```

### **Step 7: Run the Application**

Start the Uvicorn server, making it accessible from the internet.

```bash
# Run the Uvicorn server
# The host 0.0.0.0 makes it publicly accessible
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

### **Accessing Your API**

Your API is now live! You can access it from Postman or any other client using your server's public IP address:

`http://<YOUR_SERVER_IP>:8000/matex/completed-check`

### **For Production Use (Post-Demo)**

This setup is for demonstration purposes. For a production environment, you should use a more robust stack:

1.  **Gunicorn**: A production-grade process manager to run Uvicorn workers.
2.  **Systemd**: A service manager to run Gunicorn in the background and ensure it starts on boot.
3.  **Nginx**: A reverse proxy to manage incoming requests, handle HTTPS/SSL, and improve security.

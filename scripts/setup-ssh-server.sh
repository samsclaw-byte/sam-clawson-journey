#!/bin/bash
# SSH Server Setup for WSL

echo "Installing OpenSSH server..."
sudo apt update
sudo apt install -y openssh-server

echo "Configuring SSH..."
sudo mkdir -p /var/run/sshd
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

echo "Starting SSH service..."
sudo service ssh start

echo "Adding auto-start to .bashrc..."
if ! grep -q "sudo service ssh start" ~/.bashrc; then
    echo 'sudo service ssh start 2>/dev/null || true' >> ~/.bashrc
fi

echo "SSH server setup complete!"
sudo service ssh status

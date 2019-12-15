cd ~/Documents/GitHub
git clone https://github.com/Azure/azure-cli.git
cd azure-cli
sudo docker build --build-arg PYTHON_VERSION=3.8.0 -f Dockerfile .
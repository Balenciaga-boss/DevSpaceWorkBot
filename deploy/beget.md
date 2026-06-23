# Beget VPS Deploy

## 1. Install Docker

```bash
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 2. Upload Project

```bash
sudo mkdir -p /opt/devspace-bot
sudo chown -R "$USER":"$USER" /opt/devspace-bot
cd /opt/devspace-bot
```

Copy project files into `/opt/devspace-bot`.

## 3. Create Environment

```bash
cp .env.beget.example .env
nano .env
```

Required values:

```env
BOT_TOKEN=your_bot_token
ADMIN_CHAT_ID=your_admin_chat_id
DATABASE_URL=mysql+asyncmy://devspace:your_mysql_password@mysql:3306/devspace_bot
MYSQL_DATABASE=devspace_bot
MYSQL_USER=devspace
MYSQL_PASSWORD=your_mysql_password
MYSQL_ROOT_PASSWORD=your_root_password
```

`DATABASE_URL` password and `MYSQL_PASSWORD` must match.

## 4. Start

```bash
docker compose up -d --build
docker compose logs -f devspace-bot
```

Expected bot log:

```text
Start polling
Run polling for bot ...
```

## 5. Update

```bash
cd /opt/devspace-bot
docker compose up -d --build
docker compose logs -f devspace-bot
```

## 6. Stop

```bash
docker compose down
```


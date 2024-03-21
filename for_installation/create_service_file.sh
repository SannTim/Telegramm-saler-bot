#!/bin/bash

SCRIPT=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")

# Путь к текущей директории
current_dir=$(dirname "$SCRIPT_DIR")

# Создаем файл .service
cat <<EOF > Telegramm-saler-bot.service
[Unit]
Description=Start Script Service
After=network.target

[Service]
Type=simple
ExecStart=$current_dir/start.sh
WorkingDirectory=$current_dir
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "Файл службы start_service.service был создан в текущей директории."


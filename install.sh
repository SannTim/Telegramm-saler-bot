#!/bin/bash
#? проверка наличия postgres на компьютере 
if [ "$(id -u)" != "0" ]; then
    echo "Этот скрипт должен быть запущен с правами суперпользователя." >&2
    exit 1
fi
#? проверка наличия Python на компьютере
if command -v python3 >/dev/null 2>&1; then
    echo "Python установлен на этом сервере."
else
    echo "Python не установлен на этом сервере."
	exit -1
fi
#? проверка наличия pipenv на компьютере
if command -v python3 >/dev/null 2>&1; then
    echo "pipenv установлен на этом сервере."
else
    echo "pipenv не установлен на этом сервере."
	exit -1
fi
SCRIPT=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")
chmod +x $SCRIPT_DIR/start.sh
chmod +x $SCRIPT_DIR/for_installation/*.sh
cd $SCRIPT_DIR/environment
source $(pipenv --venv)/bin/activate
pipenv install

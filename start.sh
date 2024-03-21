#!/bin/bash
SCRIPT=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")
#chmod +x $SCRIPT_DIR/start.sh
cd $SCRIPT_DIR/environment
source $(pipenv --venv)/bin/activate
cd $SCRIPT_DIR/data
python3 __main__.py
exit -1

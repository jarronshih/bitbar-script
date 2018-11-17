#!/bin/bash
PATH=/usr/local/bin:$PATH
PY_FILE=1p3a.py

SOURCE="${BASH_SOURCE[0]}"
TRUE_SOURCE=`readlink ${SOURCE}`
if [[ ${TRUE_SOURCE} != "" ]]; then
  FOLDER=`dirname ${TRUE_SOURCE}`
  cd ${FOLDER}
fi

pipenv run python3 ${PY_FILE}

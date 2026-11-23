#!/bin/bash
#====================================
# @file: docker-entrypoint.sh
# @brief Docker entry point
#====================================
set -e

script/build
if [ $IS_RELEASE -eq 1 ]
then
    script/package
fi

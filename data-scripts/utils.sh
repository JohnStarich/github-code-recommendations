#!/bin/bash

function error() {
    echo -e "\033[31m$@\033[m" >&2
}

function success() {
    echo -e "\033[32m$@\033[m" >&2
}

function rate_limit() {
    local RATE_LIMIT=$1
    local COMMAND=${@:2}
    if [ -z "${RATE_LIMIT}" ]; then
        error 'Please provide a number followed by a command'
        return 2
    fi
    if [ -z "${COMMAND}" ]; then
        error 'Please provide a command following the rate limit number'
        return 2
    fi
    if ! [[ ${RATE_LIMIT} =~ ^-?[0-9]+$ ]]; then
        error 'Rate limit (first argument) is not a number'
        return 2
    fi
    joblist=($(jobs -p))
    while (( ${#joblist[*]} >= "$RATE_LIMIT" )); do
        sleep 1
        joblist=($(jobs -p))
    done
    bash -c "${COMMAND}" &
    return $?
}


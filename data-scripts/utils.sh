#!/bin/bash

function error() {
    echo -e "\033[31m$@\033[m" >&2
}

function success() {
    echo -e "\033[32m$@\033[m" >&2
}


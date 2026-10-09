#!/usr/bin/env bash

# URL-encode a user-supplied string of text
# Usage: ./urlencode_script.sh
# Enter the string you want to URL encode: https://github.com/
# https%3A%2F%2Fgithub.com%2F
urlencode() {
    local LC_ALL=C
    local str="$1"
    local encoded=""
    for (( i = 0; i < ${#str}; i++ )); do
        local char="${str:i:1}"
        case "$char" in
            [a-zA-Z0-9.~_-])
                encoded+="$char"
            ;;

            *)
                encoded+="$(printf '%%%02X' "'$char")"
            ;;
        esac
    done
    echo "$encoded"
}

read -p "Enter the string you want to URL encode: " input_string
urlencode "$input_string"


#!/usr/bin/env node

const readline = require('readline');

function urlencode(s) {
    let encoded = '';
    for (let i = 0; i < s.length; i++) {
        let char = s.charAt(i);
        if (/^[a-zA-Z0-9.~_-]$/.test(char)) {
            encoded += char;
        } else {
            encoded += '%' + char.charCodeAt(0).toString(16).toUpperCase();
        }
    }
    return encoded;
}

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question("Enter the string you want to URL encode: ", function(inputString) {
    let encodedString = urlencode(inputString);
    console.log(encodedString);
    rl.close();
});

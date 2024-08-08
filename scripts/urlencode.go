package main

import (
    "fmt"
    "net/url"
    "os"
    "bufio"
)

func main() {
    reader := bufio.NewReader(os.Stdin)
    fmt.Print("Enter the string you want to URL encode: ")
    inputString, _ := reader.ReadString('\n')
    
    encodedString := urlencode(inputString)
    fmt.Println(encodedString)
}

func urlencode(str string) string {
    encoded := ""
    for _, char := range str {
        switch {
        case (char >= 'a' && char <= 'z') || (char >= 'A' && char <= 'Z') || (char >= '0' && char <= '9') || char == '.' || char == '~' || char == '-' || char == '_':
            encoded += string(char)
        default:
            encoded += fmt.Sprintf("%%%02X", char)
        }
    }
    return encoded
}

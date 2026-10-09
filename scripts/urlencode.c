#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

char* urlencode(const char* str) {
    char* encoded = malloc(strlen(str) * 3 + 1); // Allocate memory for the encoded string
    if (encoded == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    int index = 0;
    for (int i = 0; str[i] != '\0'; i++) {
        if (isalnum(str[i]) || strchr(".~-_", str[i]) != NULL) {
            encoded[index++] = str[i];
        } else {
            sprintf(encoded + index, "%%%02X", (unsigned char)str[i]);
            index += 3;
        }
    }
    encoded[index] = '\0'; // Null-terminate the string
    return encoded;
}

int main() {
    char input_string[1000];
    printf("Enter the string you want to URL encode: ");
    fgets(input_string, sizeof(input_string), stdin);
    input_string[strcspn(input_string, "\n")] = '\0'; // Remove trailing newline character
    
    char* encoded_string = urlencode(input_string);
    printf("%s\n", encoded_string);
    free(encoded_string); // Free the dynamically allocated memory
    return 0;
}

use std::io;

fn urlencode(s: &str) -> String {
    let mut encoded = String::new();
    for c in s.chars() {
        if c.is_ascii_alphanumeric() || ".~-_".contains(c) {
            encoded.push(c);
        } else {
            encoded.push_str(&format!("%{:02X}", c as u8));
        }
    }
    encoded
}

fn main() {
    println!("Enter the string you want to URL encode:");
    let mut input_string = String::new();
    io::stdin().read_line(&mut input_string).expect("Failed to read input");
    let input_string = input_string.trim_end(); // Remove trailing newline character
    
    let encoded_string = urlencode(input_string);
    println!("{}", encoded_string);
}

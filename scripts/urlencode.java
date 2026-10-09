import java.util.Scanner;

public class URLEncoder {

    public static String urlencode(String s) {
        StringBuilder encoded = new StringBuilder();
        for (char c : s.toCharArray()) {
            if (Character.isLetterOrDigit(c) || ".~-_".indexOf(c) != -1) {
                encoded.append(c);
            } else {
                encoded.append(String.format("%%%02X", (int) c));
            }
        }
        return encoded.toString();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter the string you want to URL encode:");
        String inputString = scanner.nextLine();
        String encodedString = urlencode(inputString);
        System.out.println(encodedString);
        scanner.close();
    }
}

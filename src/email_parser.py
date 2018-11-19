import re


class EmailParser(object):
    """Retrieve all emails from text."""
    email_pattern = re.compile(r'\w[\w\.-]*@\w[\w\.-]+\.\w+')

    def __init__(self, forbidden=('^webmaster@', '^hostmaster@', '^postmaster@', '^support@',
                                  '.png$', '.jpg$', '.jpeg$', '.gif$')):
        self.forbidden = [re.compile(pattern) for pattern in forbidden]

    def is_forbidden(self, email):
        """Check that email is forbidden."""
        email_lower = email.lower()
        for pattern in self.forbidden:
            if pattern.search(email_lower):
                return True
        return False

    def get_emails(self, text):
        """Find all emails in text except forbidden."""
        emails = self.email_pattern.findall(text)
        emails = [email for email in emails if not self.is_forbidden(email)]
        return list(set(emails))


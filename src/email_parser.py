import re


class EmailParser(object):
    """Retrieve all emails from text."""
    email_pattern = re.compile(r'\w[\w\.-]*@\w[\w\.-]+\.\w+')

    def __init__(self, forbidden=('webmaster@', 'hostmaster@', 'postmaster@', 'support@')):
        self.forbidden = forbidden

    def is_forbidden(self, email):
        """Check that email is forbidden."""
        email_lower = email.lower()
        for forbid in self.forbidden:
            if forbid in email_lower:
                return True
        return False

    def get_emails(self, text):
        """Find all emails in text except forbidden."""
        emails = self.email_pattern.findall(text)
        emails = [email for email in emails if not self.is_forbidden(email)]
        return emails


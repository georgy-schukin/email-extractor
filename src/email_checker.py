#!/usr/bin/env python

import smtplib
import dns.resolver


def read_lines(input_file):
    with open(input_file, "r") as f:
        return [line.strip('\n') for line in f.readlines()]


def write_lines(output_file, lines):
    with open(output_file, "w") as f:
        for line in lines:
            f.write(line + "\n")


def check_emails(emails):
    verified = []
    unverified = []
    for email in emails:
        if check_email(email):
            verified.append(email)
        else:
            unverified.append(email)
    return verified, unverified


def check_email(email):
    domain = email.split('@')[1]
    mx_record = str(dns.resolver.query(domain, 'MX')[0].exchange)
    try:
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mx_record)
        code, _ = server.verify(email)
        server.quit()
        return code == 250
    except Exception as e:
        print("Error: " + str(e))
    return False


def main():
    email = input("Email: ")
    print("Ok") if check_email(email) else print("Not Ok")
    #emails = read_lines("emails.txt")
    #verified, unverified = check_emails(emails)
    #write_lines("verified_emails.txt", verified)
    #write_lines("unverified_emails.txt", unverified)


if __name__ == '__main__':
    main()
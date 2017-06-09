import re

failed_pattern          = re.compile("^\*\*\*.*$")
null_author             = re.compile("^<>$")
visier_prepended        = re.compile("^VISIER\\.*$")
full_name_no_email      = re.compile("^([A-Z]\w*\s?)+$")
full_name_null_email    = re.compile("^([A-Z]\w*\s?)+<>$")
full_name_with_email    = re.compile("^([A-Z]\w*\s?)+<.*>$")
username_no_email       = re.compile("^\w*$")
username_null_email     = re.compile("^\w*\s?<>$")
username_with_email     = re.compile("^\w*\s?<.*>$")
username_sqr_email      = re.compile("^\w*\s?\[.*\]$")
username_rnd_name       = re.compile("^\w*\s?\(.*\)$")
username_address        = re.compile("^\w*@.*$")
any_any                 = re.compile("^.+<.*>$")
null_any                = re.compile("^<.*>$")
any_email               = re.compile("^.+\s\S+@\S+$")
any_null                = re.compile("^.+$")


def email_from_fullname(author):
    return "email for " + author

def email_from_username(author):
    return "email for " + author

def username_from_email(author):
    return "dummy_username for " + author

def replace_author(author):
    if failed_pattern.match(author):
        return "nulluser <>"
    if null_author.match(author):
        return "nulluser " + author
    if visier_prepended.match(author):
        return replace_author(author[7:])
    if full_name_no_email.match(author):
        return author.strip() + " <{}>".format(email_from_fullname(author.strip()))
    if full_name_null_email.match(author):
        fullname = author.strip()[:-2].strip()
        return fullname + " <{}>".format(email_from_fullname(fullname))
    if full_name_with_email.match(author):
        return author
    if username_no_email.match(author):
        return author.strip() + " <{}>".format(email_from_username(author.strip()))
    if username_null_email.match(author):
        username = author.strip()[:-2].strip()
        return username + " <{}>".format(email_from_username(username))
    if username_with_email.match(author):
        return author
    if username_sqr_email.match(author):
        return author.replace("[", "<").replace("]", ">")
    if username_rnd_name.match(author):
        username = author.split("(")[0].strip()
        return username + " " + email_from_username(username)
    if username_address.match(author):
        username = author.split("@")[0]
        return username + " <{}>".format(email_from_username(username))
    if any_any.match(author):
        return author
    if null_any.match(author):
        return username_from_email(author[1:-1]) + " " + author
    if any_email.match(author):
        email = author.split(" ")[-1].strip()
        return author.replace(email, "<{}>".format(email))
    if any_null.match(author):
        return "nulluser <>"

in_authors  = open("authors.txt", "r")
out_authors = open("reformatted-authors.txt", "w")
for author in in_authors:
    out_authors.write("{0}={1}\n".format(author.strip(), replace_author(author).strip()))
in_authors.close()
out_authors.close()

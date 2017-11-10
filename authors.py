import re
import csv
import os

failed_pattern          = re.compile("^\*\*\*.*$")
null_author             = re.compile("^<>$")
visier_prepended        = re.compile("^VISIER\\\.*$")
full_name_no_email      = re.compile("^([A-Z][\w\-]*\s?)+$")
full_name_null_email    = re.compile("^([A-Z][\w\-]*\s?)+<>$")
full_name_with_email    = re.compile("^([A-Z][\w\-]*\s?)+<.+>$")
username_no_email       = re.compile("^[\w\-]*$")
username_null_email     = re.compile("^[\w\-]*\s?<>$")
username_with_email     = re.compile("^[\w\-]*\s?<.+>$")
username_sqr_email      = re.compile("^[\w\-]*\s?\[.*\]$")
username_rnd_name       = re.compile("^[\w\-]*\s?\(.*\)$")
username_address        = re.compile("^[\w\-]*@.*$")
first_last_name         = re.compile("^[\w\-]*\.[\w\-]*$")
any_any                 = re.compile("^.+<.*>$")
null_any                = re.compile("^<.*>$")
any_email               = re.compile("^.+\s\S+@\S+$")
any_null                = re.compile("^.+$")

with open(os.path.dirname(os.path.abspath(__file__)) + "/users.csv", "r") as users_file:
    users_reader = csv.reader(users_file, delimiter=',')
    users = [{"name": user[0], "username": user[1], "email": user[2]} for user in users_reader]

def email_from_fullname(author):
    return next((user["email"] for user in users if user["name"].lower() == author.lower()), "")

def email_from_username(author):
    return next((user["email"] for user in users if user["username"].lower() == author.lower()), "")

def username_from_email(author):
    return next((user["username"] for user in users if user["email"].lower() == author.lower()), "")

def username_from_fullname(author):
    return next((user["username"] for user in users if user["name"].lower() == author.lower()), "")

def username_from_firstname_lastname(author):
    return next((user["username"] for user in users if user["name"].lower() == author.replace(".", " ").lower()), "")

def replace_author(author):
    if failed_pattern.match(author):
        return "nulluser <>"
    if null_author.match(author):
        return "nulluser " + author
    if visier_prepended.match(author):
        return replace_author(author[7:])
    if full_name_with_email.match(author):
        fullname = author.split("<")[0].strip()
        email = author.split("<")[1].split(">")[0].strip()
        username = username_from_email(email)
        return (username if username else fullname) + " <{}>".format(email)
    if full_name_null_email.match(author):
        fullname = author.strip()[:-2].strip()
        return username_from_fullname(fullname) + " <{}>".format(email_from_fullname(fullname))
    if full_name_no_email.match(author):
        username = username_from_fullname(author.strip())
        return (username if username else author.strip()) + " <{}>".format(email_from_fullname(author.strip()))
    if username_with_email.match(author):
        return author
    if username_null_email.match(author):
        username = author.strip()[:-2].strip()
        return username + " <{}>".format(email_from_username(username))
    if username_no_email.match(author):
        return author.strip() + " <{}>".format(email_from_username(author.strip()))
    if username_sqr_email.match(author):
        return author.replace("[", "<").replace("]", ">")
    if username_rnd_name.match(author):
        username = author.split("(")[0].strip()
        return username + " <{}>".format(email_from_username(username))
    if username_address.match(author):
        username = author.split("@")[0]
        return username + " <{}>".format(email_from_username(username))
    if first_last_name.match(author):
        username = username_from_firstname_lastname(author)
        return (username if username else author.strip()) + " <{}>".format(email_from_username(username))
    if any_any.match(author):
        return author
    if null_any.match(author):
        return username_from_email(author[1:-1]) + " " + author
    if any_email.match(author):
        bad_email = author.split(" ")[-1]
        email = bad_email.strip().replace("<", "").replace(">", "")
        return author.replace(bad_email, "<{}>".format(email))
    if any_null.match(author):
        return "nulluser <>"

with open("authors.txt", "r") as in_authors, open("reformatted-authors.txt", "w") as out_authors:
    for author in in_authors:
        out_authors.write("\"{0}\"=\"{1}\"\n".format(author.strip(), replace_author(author).strip()))

import re

# FIX MAIN.PY
with open("main.py", "r") as f:
    text = f.read()

# 1. We need to save the IMAP connection or provide a way to mark seen.
# Actually, the best way: in fetch_cdc_emails, instead of closing the mail connection, return it.
text = text.replace('mail.close()\n    mail.logout()\n    return extracted_jobs', 'return extracted_jobs, mail')

# 2. Add 'eid' to extracted jobs
text = text.replace('"pdfs": pdfs\n                    })', '"pdfs": pdfs,\n                        "eid": eid\n                    })')

# 3. In main(), receive mail object
text = text.replace('jobs = fetch_cdc_emails()', 'jobs_data = fetch_cdc_emails()\n    if not jobs_data: return\n    if isinstance(jobs_data, tuple): jobs, mail = jobs_data\n    else: jobs, mail = jobs_data, None')

# 4. Process and mark seen
mark_seen_code = """
                if mail and 'eid' in job:
                    mail.store(job['eid'], '+FLAGS', '\\\\Seen')
                    print(f"Marked {job['eid']} as seen.")
"""
text = text.replace('generate_dashboard.generate()', f'generate_dashboard.generate()\n{mark_seen_code}')

# Close mail at the end
end_code = """
    if mail:
        try:
            mail.close()
            mail.logout()
        except: pass
"""
text = text.replace('if __name__ == "__main__":', f'{end_code}\nif __name__ == "__main__":')

with open("main.py", "w") as f:
    f.write(text)


# FIX SHORTLIST_BOT.PY
with open("shortlist_bot.py", "r") as f:
    text2 = f.read()

text2 = text2.replace('mail.close()\n    mail.logout()\n    return matched_emails', 'return matched_emails, mail')
text2 = text2.replace('"pdfs": pdf_paths\n                })', '"pdfs": pdf_paths,\n                    "eid": num\n                })')

# In process_emails
text2 = text2.replace('emails = check_for_shortlists()', 'emails_data = check_for_shortlists()\n    if not emails_data: return\n    if isinstance(emails_data, tuple): emails, mail = emails_data\n    else: emails, mail = emails_data, None')

mark_seen_code2 = """
                if mail and 'eid' in email_obj:
                    mail.store(email_obj['eid'], '+FLAGS', '\\\\Seen')
"""
text2 = text2.replace('generate_dashboard.generate()', f'generate_dashboard.generate()\n{mark_seen_code2}')

end_code2 = """
    if mail:
        try:
            mail.close()
            mail.logout()
        except: pass
"""
text2 = text2.replace('if __name__ == "__main__":', f'{end_code2}\nif __name__ == "__main__":')

with open("shortlist_bot.py", "w") as f:
    f.write(text2)


"""
email_sender.py

A module to generate and send an email with embedded images, tracebacks, and attachments using Outlook via pywin32.
"""

import os
import win32com.client as win32


def send_email_with_embedded_images(
    tracebacks_html, image_paths, attachment_paths, subject, to, cc=None, bcc=None
):
    """
    Send an email using Outlook with embedded images, tracebacks, and attachments.

    :param tracebacks_html: List of tracebacks as HTML strings.
    :param image_paths: List of image file paths to embed in the email.
    :param attachment_paths: List of file paths to attach to the email.
    :param subject: Email subject.
    :param to: Recipient email address(es), separated by semicolons if multiple.
    :param cc: (Optional) CC email address(es), separated by semicolons if multiple.
    :param bcc: (Optional) BCC email address(es), separated by semicolons if multiple.
    """

    # Initialize Outlook application
    outlook = win32.Dispatch("Outlook.Application")

    # Create a new mail item
    mail = outlook.CreateItem(0)  # 0: olMailItem

    # Set email properties
    mail.Subject = subject
    mail.To = to
    if cc:
        mail.CC = cc
    if bcc:
        mail.BCC = bcc

    # Build the HTML body
    html_body = "<html><body>"

    # Add tracebacks
    for idx, tb_html in enumerate(tracebacks_html, 1):
        html_body += f'<div class="error"><h2>Error {idx}</h2>{tb_html}</div><br>'

    # Add images with CIDs
    image_cids = {}
    for idx, image_path in enumerate(image_paths):
        cid = f"image{idx}"
        image_cids[image_path] = cid
        html_body += f'<div class="image"><img src="cid:{cid}"></div><br>'

    html_body += "</body></html>"

    # Set the HTML body
    mail.HTMLBody = html_body

    # Attach images and set the CID
    for image_path, cid in image_cids.items():
        if os.path.isfile(image_path):
            attachment = mail.Attachments.Add(image_path)
            # Set the Content-ID (CID) of the attachment
            attachment.PropertyAccessor.SetProperty(
                "http://schemas.microsoft.com/mapi/proptag/0x3712001F", cid
            )
        else:
            print(f"Image file not found: {image_path}")

    # Attach other attachments (e.g., spreadsheets)
    for attachment_path in attachment_paths:
        if os.path.isfile(attachment_path):
            mail.Attachments.Add(attachment_path)
        else:
            print(f"Attachment file not found: {attachment_path}")

    # Send the email
    mail.Send()

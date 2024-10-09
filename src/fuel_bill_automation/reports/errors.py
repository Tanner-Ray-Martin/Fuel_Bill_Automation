"""
error_reporter.py

A module to generate an HTML document from a list of traceback information or custom error messages.
This HTML document can be used as the body of an email to report errors.
"""

import html


def generate_error_email_body(errors, title="Error Report"):
    """
    Generate an HTML document from a list of errors.

    :param errors: List of error messages or traceback strings.
    :param title: (Optional) Title of the error report.
    :return: A string containing the HTML document.
    """
    # Start the HTML document
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{html.escape(title)}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        h1 {{
            color: #d9534f;
        }}
        pre {{
            background-color: #f9f9f9;
            border: 1px solid #e1e1e8;
            padding: 10px;
            overflow-x: auto;
        }}
        .error {{
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <h1>{html.escape(title)}</h1>
"""

    # Add each error to the HTML body
    for idx, error in enumerate(errors, 1):
        escaped_error = html.escape(error)
        html_content += f"""
    <div class="error">
        <h2>Error {idx}</h2>
        <pre>{escaped_error}</pre>
    </div>
"""
    # Close the HTML document
    html_content += """
</body>
</html>
"""
    return html_content

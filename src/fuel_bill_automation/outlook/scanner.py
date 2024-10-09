import os
import win32com.client


def save_attachments_from_inbox(search_word: str, file_extension: str, save_path: str):
    # Ensure the save_path exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Connect to Outlook
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox
    messages = inbox.Items

    for message in messages:
        if message.Class == 43:  # 43 is the class type for mail items
            try:
                # Check if the message has attachments
                if message.Attachments.Count > 0:
                    # Loop through all attachments
                    for attachment in message.Attachments:
                        attachment_name = attachment.FileName
                        # Check if attachment name contains the search_word and has the correct file extension
                        if search_word in attachment_name and attachment_name.endswith(
                            file_extension
                        ):
                            # Save the attachment to the specified folder
                            attachment.SaveAsFile(
                                os.path.join(save_path, attachment_name)
                            )
                            print(f"Saved: {attachment_name}")
            except Exception as e:
                print(f"Error processing message: {str(e)}")


if __name__ == "__main__":
    search_word = input("Enter the word to search in attachments: ")
    file_extension = input("Enter the file extension (e.g., .pdf, .docx): ")
    save_path = input("Enter the folder path where attachments should be saved: ")

    save_attachments_from_inbox(search_word, file_extension, save_path)

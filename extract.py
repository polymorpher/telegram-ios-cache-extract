import os
from dotenv import load_dotenv
from iphone_backup_decrypt import EncryptedBackup, RelativePath, MatchFiles

load_dotenv()

passphrase = os.environ.get("KEY") # Or load passphrase more securely from stdin, or a file, etc.
backup_path = os.environ.get("BACKUP_PATH")

print(backup_path)
backup = EncryptedBackup(backup_directory=backup_path, passphrase=passphrase)
def save_manifest_db(backup, output_path="./output/Manifest.db"):
    """
    Save the decrypted Manifest.db file for inspection.
    
    Args:
        backup: An EncryptedBackup instance
        output_path: Path where to save the Manifest.db file
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"Saving decrypted Manifest.db to {output_path}...")
    try:
        backup.save_manifest_file(output_path)
        print(f"Manifest.db saved successfully. Please inspect this file to find correct domains and paths.")
        return True
    except Exception as e:
        print(f"Could not save Manifest.db: {e}")
        return False

# Example usage:
# save_manifest_db(backup)
# backup.extract_file(relative_path=RelativePath.CALL_HISTORY, 
#                     output_filename="./output/call_history.sqlite")

def extract_telegram_files(backup, domain_pattern="AppDomain-ph.telegra.Telegraph", path_pattern="%", output_folder="./output/telegram_files/"):
    """
    Extract Telegram files from an iPhone backup.
    
    Args:
        backup: An EncryptedBackup instance
        domain_pattern: The domain pattern to match Telegram files
        path_pattern: The path pattern to match specific files
        output_folder: Folder where to save extracted files
        
    Returns:
        int: Number of files extracted
    """
    def progress_callback(*, n, total_files, relative_path, domain, file_id, **kwargs):
        print(f"Extracting file {n} of {total_files} from {relative_path} in {domain} with file_id {file_id}")
        return True
    
    print(f"Attempting to extract Telegram files from domain '{domain_pattern}' with LIKE pattern: '{path_pattern}'")
    num_files_extracted = backup.extract_files(
        domain_like=domain_pattern, 
        relative_paths_like=path_pattern,
        filter_callback=progress_callback,
        output_folder=output_folder
    )
    print(f"Extracted {num_files_extracted} files matching the pattern.")
    return num_files_extracted

# Example usage:
# extract_telegram_files(backup)

# Example: If you wanted to extract based on another pattern, you'd call the function again
# extract_telegram_files(
#     backup,
#     path_pattern="telegram-data/postbox/db/%sqlite%",
#     output_folder="./output/telegram_db/"
# )

def extract_single_file_from_backup(backup, relative_path, output_filename, domain_like=None):
    """
    Extracts a single file from an iPhone backup.

    Args:
        backup: An EncryptedBackup instance.
        relative_path: The iOS 'relativePath' of the file to be decrypted.
                       Common relative paths are provided by the 'RelativePath' class.
        output_filename: The filename to write the decrypted file contents to.
        domain_like: Optional. The iOS 'domain' for the file to be decrypted.
                     Common domain wildcards are provided by the 'DomainLike' class.

    Returns:
        bool: True if extraction was successful, False otherwise.
    """
    try:
        print(f"Attempting to extract file '{relative_path}'" +
              (f" from domain '{domain_like}'" if domain_like else "") +
              f" to '{output_filename}'...")
        
        backup.extract_file(
            relative_path=relative_path,
            domain_like=domain_like,
            output_filename=output_filename
        )
        print(f"File '{relative_path}' extracted successfully to '{output_filename}'.")
        return True
    except Exception as e:
        print(f"Could not extract file '{relative_path}': {e}")
        return False

# Example usage:
# from iphone_backup_decrypt.utils import RelativePath, DomainLike
# extract_single_file_from_backup(
#     backup,
#     relative_path=RelativePath.TEXT_MESSAGES,
#     output_filename="./output/sms.db"
# )
#
# extract_single_file_from_backup(
#     backup,
#     relative_path="ChatStorage.sqlite", # WhatsApp messages
#     domain_like=DomainLike.WHATSAPP,
#     output_filename="./output/whatsapp_chatstorage.sqlite"
# )

# extract_single_file_from_backup(backup, "Library/Mobile Documents/com~apple~CloudDocs/telegram-chat-gatekeep.md", "./output/test.md")

extract_telegram_files(backup)
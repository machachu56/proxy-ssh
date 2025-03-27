import paramiko


def uploadtosrv(remote_folder):
    # Configuration for your SSH connection
    hostname = "your_server_ip_or_hostname"
    port = 22  # default SSH port
    username = "your_username"
    password = "your_password"  # or use key-based authentication for more security

    # Local and remote paths
    local_file_path = "./proxies.txt"
    remote_folder = "/path/to/remote/folder"
    remote_file_path = f"{remote_folder}/proxies.txt"
    remote_script_path = f"{remote_folder}/script.sh"  # bash script you want to execute

    try:
        # Create an SSH client instance
        ssh = paramiko.SSHClient()
        # Automatically add the remote server's SSH key (use with caution)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the remote server
        ssh.connect(hostname, port=port, username=username, password=password)
        print("SSH connection established.")

        # Open an SFTP session and upload the file
        sftp = ssh.open_sftp()
        sftp.put(local_file_path, remote_file_path)
        print(f"File uploaded to {remote_file_path}.")
        sftp.close()

        # Execute the bash script on the remote server
        # Ensure that the script has executable permissions (chmod +x script.sh)
        command = f"bash {remote_script_path}"
        stdin, stdout, stderr = ssh.exec_command(command)

        # Optionally, capture and print the output and errors from the script execution
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if output:
            print("Script Output:")
            print(output)
        if error:
            print("Script Errors:")
            print(error)
        
    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Close the SSH connection
        ssh.close()
        print("SSH connection closed.")

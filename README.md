# RNA-Structure-Hub
How to Access & Clone moss-lab/RNA-Structure-Hub (Private Repository)

Follow these steps to set up SSH access and clone the private repository.
🚀 Step 1: Generate a New SSH Key

Run the following command, replacing "your_email@example.com" with your GitHub email:

ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

    Press Enter to save it in the default location (~/.ssh/id_rsa).
    Press Enter again to leave the passphrase empty.

🚀 Step 2: Add the SSH Key to GitHub

    Copy your public key:

    cat ~/.ssh/id_rsa.pub

    Go to GitHub → Settings → SSH and GPG keys: 🔗 Click Here

    Click "New SSH Key", set a title (e.g., "Lab SSH Key"), paste the key, and save.

🚀 Step 3: Test the SSH Connection

Run:

ssh -T git@github.com

If it works, you should see:

Hi YOUR_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.

🚀 Step 4: Clone the Repository

Now, clone the private repository using SSH:

git clone git@github.com:moss-lab/RNA-Structure-Hub.git

🚀 Step 5: Configure SSH for GitHub (If Needed)

If the cloning fails due to multiple SSH keys, create a configuration file:

    Open the SSH config file:

nano ~/.ssh/config

Add the following lines:

Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa
    IdentitiesOnly yes

Save and exit (Ctrl + X, then Y, then Enter).

Restart the SSH agent:

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

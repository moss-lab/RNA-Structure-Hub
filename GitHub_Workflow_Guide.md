**Welcome to this repository! Below are the basic GitHub commands and workflows for working with this project.**

## 📥 Cloning the Repository
To get a local copy of this repository, use the following command:
```bash
git clone git@github.com:moss-lab/RNA-Structure-Hub.git
cd RNA-Structure-Hub

🔄 Pulling the Latest Changes

Before making any changes, always pull the latest updates:

git pull origin main

✏️ Making Changes and Committing Them

    Create a new branch for your changes (never commit directly to main):

git checkout -b my-feature-branch

Make changes to the files in the repository.
Stage the changes (prepare them for commit):

git add .

Commit the changes with a message:

    git commit -m "Describe what you changed"

📂 Handling Large Files (Optional)

If you need to commit large files, use Git Large File Storage (LFS):

git lfs track "*.file-extension"
git add .gitattributes
git add <large-file>
git commit -m "Added large file using Git LFS"

🚀 Note: Install Git LFS first if you haven’t:

git lfs install

🚀 Pushing Your Changes

After committing your changes, push your new branch to GitHub:

git push origin my-feature-branch

🔄 Creating a Pull Request (PR)

    Go to the repository on GitHub.
    Click Pull Requests → New Pull Request.
    Select your branch (my-feature-branch) as the source and main as the target.
    Add a description and click "Create Pull Request".
    Wait for at least one approval before merging.

✅ Approving & Merging a Pull Request

    A team member will review the pull request.
    If changes are needed, the reviewer will request updates.
    Once approved:
        Click "Merge Pull Request".
        Delete the branch if it’s no longer needed.

🎉 Congratulations! You've successfully contributed to this project! If you have any questions, reach out to the team. 🚀

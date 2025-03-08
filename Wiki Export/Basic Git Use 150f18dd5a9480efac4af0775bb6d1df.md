# Basic Git Use

Author: Aaliyah Yan
Branch: Hardware
Hidden: No
Parent page: Development Resources (Development%20Resources%2014bf18dd5a9480dcb4cbfec87e0cb38b.md)

[Intro to Git Workshop.pdf](Basic%20Git%20Use%20150f18dd5a9480efac4af0775bb6d1df/Intro_to_Git_Workshop.pdf)

1. The above workshop details all of the terminology and commands that you’ll need to use for Git in Generate
2. First, make sure you have [Git installed and setup on your machine](https://generate-hardware.atlassian.net/wiki/spaces/KB/pages/3276801)

If you need to clone the remote repository to your machine

- If you need to clone the remote repository to your machine
    
    Next, you’ll need to clone the remote repo onto your local machine. To do that:
    
    1. Navigate to the Github page for the repo that you want to use
    2. Click the green “<> Code” dropdown button
        1. If you have SSH keys installed and setup, click on the “SSH” tab, otherwise keep it on the “HTTPS” tab
        2. Copy the link shown
    3. Open a terminal window on your computer and navigate to the directory where you want to clone the repo
        1. Run the following command:
        
        ```jsx
        git clone <PASTE_YOUR_LINK_HERE>
        ```
        
        1. Assuming no errors show up, you’ve successfully cloned the repo!
        
- Now to actually use Git to track your project
    1. **Before doing any work, make sure that you’re on the correct Git branch.** If you’re not:
        1. If you don’t have the correct branch on your machine:
            1. In the terminal, run this command to see a list of all braches (local and remote)
            
            ```jsx
            git branch -a
            ```
            
            1. To get a remote branch on your machine to do work, run 
            
            ```jsx
            git fetch BRANCH_NAME
            ```
            
        2. If you already fetched the branch and just need to switch to it, run 
        
        ```jsx
        git switch BRANCH_NAME
        ```
        
    2. Whenever you make a significant change to a file (code, schematic, or layout), you’ll want to “commit” those changes to the remote repo. To do this:
        1. Command Line:
            1. Use the following command to check what files have been changed 
            2. 
                1. The names of changed files will be shown in red
            
            ```jsx
            git status
            ```
            
            1. To add a file to the staging area (this is the area that tells git what files to actually track), run 
            
            ```jsx
            git add FILE_NAME
            ```
            
            1. Once you’ve added all of the files that you want to the staging area, run 
            
            ```jsx
            git commit -m "type a nice message here describing what was changed and why"
            ```
            
            1. Then type the following command to push your changes to the remote repo 
            
            ```jsx
            git push
            ```
            
        2. GitHub Desktop:
            1. **Make sure that you only select the files that are important for everyone to have a copy of**
            2. Write a message in the box at the bottom left-hand corner of the app, and then hit the “commit” button
# Git Guidelines

Author: Alex Nikanov
Branch: Software
Hidden: No
Parent page: Dev Best Practice (Dev%20Best%20Practice%20365b0c30e6ac4885b80bf0a3e2f5749f.md)

[https://www.loom.com/share/ae3b496b3c8641f8a931e6e4414fac1d](https://www.loom.com/share/ae3b496b3c8641f8a931e6e4414fac1d)

# What is Git?

Git is a version control system. At a high level, one can think of it as a timeline management utility for your codebase. All of your code can be backed up in different versions, at different time points, so that any code modifications are safe and the codebase can be reverted to a specific point if a bug is introduced.

Note that GitHub, GitLab, and Bitbucket are specific platforms that host code and are based on Git.

# How do I install Git?

[https://www.loom.com/share/4e8ed6bef63a44c4b3710f28605cf515](https://www.loom.com/share/4e8ed6bef63a44c4b3710f28605cf515)

[https://git-scm.com/book/en/v2/Getting-Started-Installing-Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Apart from installing Git in the system, you would need to clone the specific repository you will be working on to your system. This repository will be a part of the GenerateNU organization on GitHub. 

```bash
git init <project directory>
git clone <repo url> #git@HOSTNAME:USERNAME/REPONAME.git
```

You can read how to initiate and clone a repository in details through this link: [https://www.atlassian.com/git/tutorials/setting-up-a-repository](https://www.atlassian.com/git/tutorials/setting-up-a-repository).

<aside>
❗ **Additionally, you could install Git as an extension for your respective IDE (a lot of them also include it out-of-the-box), making the process considerably easier.**

</aside>

# Overall Git Workflow

[https://www.loom.com/share/3585716bb8d04fd193826b92bd78076b](https://www.loom.com/share/3585716bb8d04fd193826b92bd78076b)

In Generate, we normally use the `git feature branch` workflow, which you can read more about below or with the following link: [https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow). 

We also have this helpful graphic that summarized the workflow:

![Untitled](Git%20Guidelines%2009c801d172434d59b9bd0b62c746d5fb/Untitled.png)

## Branches `git checkout <branch>`

One of the most important Git concept you need to be comfortable with is **branches.** A branch is a version of a codebase, that started at a specific timepoint from the **original branch**, and then the code that follows in that version may **branch off** from the code in the original version.

The cool thing about Git is that you can have all those version stored at the same time — you just need to switch between them to see those versions with the following command:

```bash
git checkout <branch name>
```

There are three main branch types that you will need to understand: `main`, `dev`, and `feature-x` branches. 

For a detailed tutorial on Git branching, check out this page: [https://www.atlassian.com/git/tutorials/using-branches](https://www.atlassian.com/git/tutorials/using-branches).

### Main branch

The `main` branch stores the latest release of the codebase. That means that the code stored will likely be used in production or relayed to the client. The code that is stored here **must** compile and correspond to the design/coding standards set by the team. 

<aside>
❗ **`main` branch will be protected: that means that you will not be able to push to the branch directly, and the only way that the code in this branch will be updates is through the PRs from the `dev` branch (read on for details). This ensures the safety of the code in the branch.**

</aside>

### Dev branch

The `dev` branch is used for development (often called a “staging” branch) — it will contain the latest finished work done by the team, including some of the changes/features that are not yet ready to be released and published in the `main` branch. 

<aside>
❗ **When working on a specific ticket, you should not be working in the `dev` branch directly — make sure to pull the code from `dev`, and branch off to a feature-specific version of code.**

</aside>

### Feature branches

Note that I said “branch**es**”: there may be multiple features branches active at the same time. Throughout the semester, you will be assigned (in small teams) tickets that ask you to implement a certain feature or fix a certain bug. To do so, you will branch off `dev` branch and create a new branch that you will be working on. When you are done with your feature/bug, you will open a **pull request** from your feature branch to the `dev` branch, so your feature can be merged back into `dev`. 

We use the following naming convention for the branch names: `<group>/<ticket number>-<description>`. 

The `group` is either:

- `feature`, if you are implementing a feature
- `bug`, if you are fixing a bug

The `ticket number` is **optional**, and you may have one in the ticket tracking system your PL will use.

Finally, the `description` is a few **lowercase** words separated by **hyphens** (-), that briefly describe the feature or a bug you are implementing.

**Some examples:**

- `feature/10-sign-in-screen` (with the ticket number)
- `feature/sign-out-screen` (without the ticket number)
- `bug/15-aws-integration` (fixing the AWS integration, refer to ticket 15)

<aside>
❗ **Avoid undescriptive or long branch names such as `bug/screen` or `feature/23-adding-the-sign-in-screen-with-better-design-to-the-home-page`.**

</aside>

## Commits `git commit -m <commit message>`

`git commit` is one of the primary functions in Git, allowing you to record changes made since the last backup point, and submit all those changes under a common message explaining the changes made. 

### How often should I commit?

Product development is all about **small, incremental changes.** When you commit, a good rule of thumb is a single implemented feature/fixed bug/changes in dependencies, etc. Basically, your commit should be dedicated to one thing, and one thing only. 

That said, however, committing a change in a single line of comments is probably unnecessary, as that clutters the timeline. Adding a feature that involved a LOT of changes in a single commit is not a good idea either — if such a situation happens, try to break the feature down in smaller parts and work on them incrementally.

<aside>
❗ **Before committing, make sure that your code compiles and works!**

</aside>

### Writing a good commit message

There are many standards used in writing commit messages, and at Generate, we use conventional commits. You can read the specifications over here: [https://www.conventionalcommits.org/en/v1.0.0-beta.2/](https://www.conventionalcommits.org/en/v1.0.0-beta.2/). Also, there are many extensions for your favorite IDEs that automate these commit messages:

- VSCode: [https://marketplace.visualstudio.com/items?itemName=vivaxy.vscode-conventional-commits](https://marketplace.visualstudio.com/items?itemName=vivaxy.vscode-conventional-commits)
- IntelliJ: [https://plugins.jetbrains.com/plugin/13389-conventional-commit](https://plugins.jetbrains.com/plugin/13389-conventional-commit)

## Pushes `git push`

A `git push` command submits and stores the version of code stored on your local machine to the `remote` (i.e., the server that hosts the code repository). 

<aside>
❗ **Remember to never directly `git push` into `main` and to always push your work at the end of the day, so that you don’t lose the work you’ve done to an accident.**

</aside>

Read more about pushing here: [https://www.atlassian.com/git/tutorials/syncing/git-push](https://www.atlassian.com/git/tutorials/syncing/git-push).

# Pull Requests & Code Reviews

Once you have pushed a change, or collection of changes, the last step is to get review from your team. This is the most important stage of the software lifecycle, and it is also the hardest to define rules for. In this section, we will lay out some general guidelines for creating, reviewing, and merging Pull Requests. 

Code reviews are one of the most important parts of the software development lifecycle. They give team members the chance to read your code, leave comments of varying degrees, request changes, and ultimately approve the change with a 🚢. In many professional settings, especially those that could have financial implications for the company, a teammate’s approval is legally required before deploying code to production! 

<aside>
❗ **Due to the nature of code reviews, the makeup of a team may dictate tweaks on code review “best” practices. This section outlines *one* way to review code, but defer to your tech or project lead for final say.**

</aside>

### What is the purpose of a PR?

A PR is a request to merge some feature code into the `main` branch, which effectively releases a new version of the code base. PRs are helpful for a variety of reasons:

1. Keep the team on the same page with changes to their codebase, regardless of who the code author is
2. Make it easy to review a new `feature`
3. Foster conversation around code changes for everyone to weigh in on and learn from
4. Allow for asynchronous iterations on proposed code changes

### When should I open a PR?

As soon as you `push` changes to a new branch, you should open a PR. There are two stages of PRs, and it’s important to respect them so that your team knows when it’s time to look at proposed code.

<aside>
❗ **Code doesn’t have to be perfect to be reviewed - get review early and often!** If you spend hours perfecting your feature before getting any review, then PR review exposes a core aspect of the feature needing to change, all that polish-time is wasted.

</aside>

1. `Draft:` PR. Once you `push` new code, you should open a draft PR. This lets your team know that “*Hey, I’m working on this new feature locally, but it’s not ready for review yet.*” At this point, anyone can see the PR, but it will not have any requested reviewers.
2. `Ready for Review` PR. Once the feature is complete, and all the `TODO` items in the associated ticket are implemented, it is time to request review from teammates. Removing the `Draft:` prefix from the PR name, and selecting relevant team members from the `Reviewers` tab on the PR lets them know that the author thinks the code is ready to go to production, and would like feedback.

### How to write a good PR description?

When creating a pull request, there are a few things to keep in mind:

1. *What stage is it in?* If the PR is still in progress, prefix the PR title with `Draft:` or `WIP:` (Work In Progress). Also, create the PR as a “*Draft Pull Request*”.
2. *What background info should the reviewer know?* Maybe you have a diagram of the workflow that this PR implements, or a design of the database table that this PR introduces. Maybe to fully understand, and eventually `Approve`, your change, the reviewer should be familiar with an earlier change. Any resources or information that the author should know about before reading your code changes should be included in the description.
3. *What problem does the code change solve?* Depending on your team, you may have a Trello card, a GitHub issue, a Jira ticket, etc. to link to which contains more information on what this change is intended to do. This is helpful to keep the PR description short, but should not be the entire description.
4. *How was this change tested?* Every change should be tested to some extent before asking someone else to look at it. If you tested the change locally, explain how. Maybe your PR includes a bunch of unit tests for new functionality. Maybe your project contains acceptance tests, and you included that. The possibilities are endless, but by including your testing strategy for the reviewer, they won’t need to worry as much about reviewing the code for bugs, and can focus on style, structure, and overall efficiency.

### Who should I request review from?

Defer to instructions from your project lead and technical lead here, but typically when you open a pull request you should request review form 2 people: your technical lead, and whoever has worked most closely with this code. If you worked alone, or with one person on it, and it’s a new chunk of code, maybe request review from whoever was involved in the data design. Or request review from someone who is working on the same feature in a different part of the stack, or the person who will be picking up the next related feature.

If you want other eyes on the code, or it’s a particularly interesting feature PR, feel free to request review from the software director & chief architect using the [Code Walk Request](https://www.notion.so/Code-Walk-Registration-4973418aa31f44e0991e2125e8dc2a97?pvs=21) form!

### How to review code?

When submitting a PR review, you will see there are options to `Comment`, `Approve`, and `Request Changes`. The goal of opening a PR is to get `Approval` from your team. The goal of reviewing a PR is to read the code, and sniff out any aspects of the code that may not be ready for the production environment. I like to group my comments in a review into three categories, ordered by severity.

- `Nit`: Comments
    
    Nit level comments are nit picks - they are comments that don’t necessarily change the functionality of a piece of code, but they may make a suggestion to make it easier to read, slightly more efficient, or more aligned with the project’s style standards. Typically, it’s up to the PR author on whether or not they want to resolve these comments, or ignore them.
    
    **Example Nit Comments:** Maybe you find a method name to be misleading, so you’ll leave a `Nit:` explaining what you expected the method to do vs. what the method actually does. Maybe your project typically names it database tables as singular nouns (like `item`), and this PR introduces a table with a plural name (like `item_prices`), so you leave a comment like *Nit: To stay in line with the rest of this project's tables, can we rename `item_prices` to `item_price`?* 
    
- Conversational Comments
    
    I don’t prefix these, but these are comments that should definitely be addressed with conversation on the PR. Sometimes they’re genuine questions, sometimes they’re inquiries about design decisions, sometimes they are comments that don’t block the PR, but are more significant than a `Nit`. 
    
    **Example Conversational Comments**: Maybe a new PR introduces an `item_price` table like in the previous example, but there are a lot of duplicate columns between this new table and the `item` table. Depending on the size of your data and the usages of this table, it’s unclear to you why the columns are duplicated, so you may leave a comment like *Why does `item_price` duplicate both the `name` and `id` columns from the pre-existing `item` table? Should these ever be different from their corresponding columns in the `item` table?* Alternatively, maybe you noticed the author re-wrote a helper function that effectively exists somewhere else in the codebase. You may leave a comment pointing them to that function, and ask if they could try to use that one to keep the codebase cleaner.
    
- `Blocking:` Comments
    
    These comments should block the PR from being merged, which can be done using the `Request Changes` button when submitting your review. The are comments about changes that you *know* are going to break some code, or do not follow the designs that this feature is supposed to implement.
    
    **Example Blocking Comments**. Extending the previous example, maybe one of the goals with the `item_price` table is to be able to handle prices in any currency, but the `item_price` table does not have a column for `currency`. You may leave a comment like *Blocking: According to the designs, we want to track prices of any currency. Should the `item_price` table have a `currency` column, or should there be a `TODO:` comment in the code to add this support later on?* Additionally, maybe you notice a boolean logic error in a function named `isItemOverPrice(int price)` that returns `this.price < price` instead of `this.price > price`. This would be a blocking change, because it will return the opposite of what you expect, and could lead to some nasty bugs. Additionally, maybe you also suggest the author write a unit test for a certain function that has particularly complicated logic, such that future contributors will not accidentally edit the complicated function and break the code. 
    

<aside>
❗ If you open up a pull request, and want eyes on it from some more experience engineers within Generate, request review from the chief architect and/or software director using the [Code Walk Registration Form](https://www.notion.so/Code-Walk-Registration-4973418aa31f44e0991e2125e8dc2a97?pvs=21)! Try to do this at least once this semester!

</aside>
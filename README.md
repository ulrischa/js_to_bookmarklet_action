# Bookmarklet Generator Action
This GitHub Action generates a JavaScript bookmarklet from a source file and updates a specified HTML file with the bookmarklet link.
It takes a js file in your github repo and inserts the converted bookmarklet code for an a href tag in a html file in same repo. You must define the js file, the target html file and the target id for inserting the bookmarklet code

## Features
- Reads a JavaScript file and wraps it in an IIFE if needed.
- Encodes the script as a bookmarklet.
- Updates an HTML file by replacing the `href` of a specific link element.
- Automatically commits and pushes the changes to the repository.

## For What?
Use this if you want to host a bookmarklet install html page on github pages. You can work with your JS and push it as usual.

## Usage

**VERY IMPORTANT: YOU NEED TO GIVE THE WORKFLOW READ AND WRITE PERMISSIONS**

![actions](https://github.com/user-attachments/assets/7a9135e0-1a2e-4658-8bca-f6bf757c800e)


To use this Action, add it to your workflow file. And change the path to your disired files and the selector in the html

```yaml
name: Test Bookmarklet Generator

on:
  push:
    branches:
      - main
    paths:
      - 'raw_js_file.js'

jobs:
  bookmarklet-job:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Use Bookmarklet Generator Action
        uses: ulrischa/js_to_bookmarklet_action@v1
        with:
          source_js_file: 'raw_js_file.js'
          target_html_file: 'install_page.htm'
          target_element_id: 'target'
          commit_message: 'Update bookmarklet link'

      - name: Debug Files and Environment
        run: |
          ls -la .
          cat raw_js_file.js
          cat install_page.htm
        shell: bash

```
## Automatically publish as github page
If you wish to automatically publish the html page as github page and use it as a install page, activate github pages:

Configure your repo as hosting for github pages. So your target html file can be reached online. Use Github Actions for this

![pages](https://github.com/user-attachments/assets/acc98043-f189-4e5a-8a85-11871cf73bd4)

Then you must change the git hub pages static.yaml action file, so that it runs after the bookmarklet conversion. Let's say you named the bookmarklet conversion action "Test Bookmarklet Generator". Then cnage the on trigger to:
```yaml
on:
  workflow_run:
    workflows:
      - Test Bookmarklet Generator
    types:
      - completed

You shoud change your static

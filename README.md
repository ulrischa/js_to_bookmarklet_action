# Bookmarklet Generator Action

This GitHub Action generates a JavaScript bookmarklet from a source file and updates a specified HTML file with the bookmarklet link.
It takes a js file in your github repo and inserts the converted bookmarklet code for an a href tag in a html file in same repo. You must define the js file, the target html file and the target id for inserting the bookmarklet code

## Features
- Reads a JavaScript file and wraps it in an IIFE if needed.
- Encodes the script as a bookmarklet.
- Updates an HTML file by replacing the `href` of a specific link element.
- Automatically commits and pushes the changes to the repository.

## Usage

To use this Action, add it to your workflow file:

```yaml
name: Use Bookmarklet Generator

on:
  push:
    branches:
      - main
    paths:
      - 'src/bookmarklet.js'

jobs:
  generate-bookmarklet:
    runs-on: ubuntu-latest
    
    steps:
      - name: Use Bookmarklet Generator
        uses: ulrischa/js_to_bookmarklet_action@v1
        with:
          source_js_file: 'src/bookmarklet.js'
          target_html_file: 'index.html'
          target_element_id: 'target'
          commit_message: 'Update bookmarklet link'



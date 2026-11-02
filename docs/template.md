# Bookmarklet Generator

Create a repository from this template, edit `src/bookmarklet.js` and push to the default branch. The starter bookmarklet displays the current page title. Supply plain JavaScript without a `javascript:` prefix.

## Installation page

1. In the new repository, select **Settings → Pages → Build and deployment → Source → GitHub Actions**.
2. Push your script or select **Actions → Build bookmarklet → Run workflow** on the default branch.
3. The workflow commits `index.htm` and publishes it as the Pages home page. The deployment job shows the published URL. Drag **Install bookmarklet** to your bookmarks bar and use it on the desired page.

The generated page takes its heading and browser title from the repository name. You may customize its text and layout. Subsequent runs update the link and the title and heading marked with `data-repo-name`. Remove that marker to keep a custom title. Keep one anchor with the configured ID and an href attribute.

The build job needs permission to push to the default branch. When Pages is disabled or uses branch publishing, the build generates the file and skips deployment. Select **GitHub Actions** as the Pages source and rerun **Build bookmarklet** to publish. The included workflow handles deployment; an additional static-site workflow would compete with it.

## Use the action in another workflow

After checking out the destination branch on an Ubuntu runner, add this step and give the job `contents: write`:

```yaml
- uses: ulrischa/js_to_bookmarklet_action@main
  with:
    source_js_file: src/bookmarklet.js
    target_html_file: index.htm
    target_element_id: target
```

For reproducible builds, pin the action to a reviewed commit. The existing v1 release predates automatic page creation. The action defaults to `index.html` when the target path is omitted.

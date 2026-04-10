# GitHub Pages Deployment

## Website URL

Your website is now published and accessible at:
**https://studentburcco43-jpg.github.io/Projecttest/**

## How It Works

The GitHub Pages deployment workflow automatically:
1. Monitors the `main` branch for changes
2. Deploys the `/Web` folder contents to GitHub Pages
3. Builds and publishes your website on every push to `main`

## Configuration Details

- **Source**: `/Web` directory
- **Branch**: Deployed from `main` branch
- **Workflow**: `.github/workflows/deploy-pages.yml`

## To View Your Website

Simply visit: **https://studentburcco43-jpg.github.io/Projecttest/**

The website will display your HTML pages, CSS styling, and JavaScript functionality.

## Making Changes

1. Edit files in the `/Web` directory
2. Commit your changes: `git add .` → `git commit -m "Update website"`
3. Push to GitHub: `git push origin main`
4. Wait for the GitHub Actions workflow to complete
5. Refresh your browser to see the changes

## Local Development

To test locally before pushing:
1. Start the FastAPI server: `python -m uvicorn API.main:app --reload`
2. Visit: `http://localhost:8000`
3. Make your changes
4. Test in the browser
5. Commit and push when ready

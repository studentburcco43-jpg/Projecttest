# Website Editing Guide

## How to Start the Server

**Press F5** or go to **Terminal → Run Build Task** to start the FastAPI server.
The terminal will display: `http://localhost:8000`

## Where to Edit Your Website

Edit these files in the **Web/** folder to customize your website:

### HTML Pages
- **Web/index.html** - Homepage (main page)
- **Web/about.html** - About page
- **Web/services.html** - Services page
- **Web/header-component.html** - Header component

### Styling
- **Web/css/site.css** - All CSS styling

### JavaScript
- **Web/js/app.js** - Website functionality

## How to Edit & View Changes

1. **Press F5** to start the server (shows link in terminal)
2. **Click the link** or visit http://localhost:8000 in your browser
3. **Edit any file** in the Web/ folder
4. **Press Ctrl+S** to save
5. **Refresh the browser** (F5 or Ctrl+R) to see your changes

## API Backend

- **API/main.py** - FastAPI app and routes
- **API/crud.py** - Database operations
- **API/schemas.py** - Data validation
- **API/database.py** - Database connection

API runs on: http://localhost:8000/api/

## Keep Server Running

The server will keep running as long as VS Code is open.
Press Ctrl+C in the terminal to stop it if needed.
Press F5 again to restart it.

# StudyBuddy - GitHub Pages Documentation

This folder contains the static website hosted on GitHub Pages for StudyBuddy.

## 📍 Website Structure

- **index.html** - Landing page with features overview and quick start
- **deployment.html** - Complete deployment guide for all platforms
- **README.md** - This file

## 🌐 GitHub Pages Setup

The site is automatically deployed to GitHub Pages from this `docs/` folder.

### Access Your Site

Your GitHub Pages site is available at:
```
https://saikrishna9603.github.io/studybuddy/
```

### Make Changes

1. Edit HTML files in this `docs/` folder
2. Commit and push to `master` branch
3. Changes are live in ~1 minute

## 🚀 Important Notes

**This is the LANDING PAGE ONLY.**

The actual StudyBuddy application (with all features) runs on a **backend server**, not GitHub Pages.

### Architecture:
```
GitHub Pages (docs/ folder)
├── Landing page
├── Documentation
└── Feature overview
        ↓
        ↓ (Links to)
        ↓
Backend Server (Railway/Render/Heroku)
├── Flask application
├── SQLite database
├── AI APIs (OpenAI + Gemini)
└── All interactive features
```

## 📚 Deploy Backend

See **deployment.html** for complete instructions on deploying the backend to:
- Railway.app ⭐ (Recommended)
- Render.com
- Heroku
- AWS/DigitalOcean
- Local machine

## 🔧 Customization

### Update Landing Page
Edit `index.html` to change:
- Hero message
- Feature cards
- Getting started steps
- Deployment options

### Add New Pages
1. Create new HTML file in `docs/` folder
2. Link from navigation in `index.html`
3. Follow the same styling and structure
4. Commit and push

## 📝 Styling

All pages use inline CSS for simplicity. For complex sites, consider:
- Separating CSS to `style.css`
- Using Bootstrap or Tailwind
- Adding JavaScript for interactivity

## 🔐 SEO & Meta Tags

Pages include:
- Meta descriptions for search engines
- Responsive viewport settings
- Open Graph tags (for social sharing)
- Proper heading hierarchy

## 📱 Responsive Design

All pages are mobile-responsive:
- Tested on 320px+ widths
- Touch-friendly buttons and links
- Readable font sizes on all devices

## 🎯 Next Steps

1. ✅ Landing page deployed to GitHub Pages
2. Deploy backend to Railway/Render (see deployment.html)
3. Update landing page with live backend URL
4. Add social media links
5. Set up custom domain (optional)

## 📖 GitHub Pages Features

- Free hosting (no credit card needed)
- Automatic HTTPS/SSL
- CDN for fast delivery
- GitHub Actions integration
- Custom domain support

## 🆘 Troubleshooting

### Page not updating after commit
- Clear browser cache (Ctrl+F5)
- Wait 1-2 minutes for GitHub Pages rebuild
- Check GitHub Pages settings in repo

### Styling looks broken
- CSS is inline in HTML files
- Check for typos in style tags
- Ensure all linked fonts load correctly

### Links returning 404
- Double-check file paths
- Use relative paths: `./page.html`
- Avoid spaces in filenames

## 📞 Support

- GitHub Issues: Report bugs or request features
- GitHub Discussions: Ask questions
- Documentation: Check deployment.html

---

**Built with ❤️ for StudyBuddy**

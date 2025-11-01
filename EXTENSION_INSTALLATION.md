# 🛡️ VeriFy Chrome Extension - Installation Guide

## 📦 Download & Installation

### Method 1: Automatic Download (Recommended)

1. **Visit the VeriFy Website**
   - Go to your VeriFy application
   - Click the **"Download Extension"** button
   - This will open the installation guide page

2. **Download the Extension**
   - Click the blue **"Download Extension ZIP"** button
   - The `verify-extension.zip` file will be downloaded automatically

3. **Extract the ZIP File**
   - Locate the downloaded `verify-extension.zip` in your Downloads folder
   - Right-click and select "Extract All..." (Windows) or double-click (Mac)
   - Choose a permanent location (e.g., `Documents/VeriFy Extension`)

4. **Install in Chrome**
   - Open Chrome browser
   - Navigate to `chrome://extensions/`
   - Enable **"Developer mode"** (toggle in top-right corner)
   - Click **"Load unpacked"**
   - Select the extracted `chrome-extension` folder
   - Click **"Select Folder"**

5. **Verify Installation**
   - You should see the VeriFy icon (🛡️) in your Chrome toolbar
   - If not visible, click the puzzle icon and pin VeriFy
   - Click the icon to start using the extension!

### Method 2: Manual Installation (For Developers)

```bash
# Clone or download the project
cd your-project-folder

# Package the extension
npm run package-extension

# The ZIP file will be created at:
# public/verify-extension.zip

# Extract and load in Chrome following steps 3-5 above
```

## 🚀 Quick Start

Once installed:

1. **Auto-Scan Mode** (Default)
   - Browse any webpage
   - VeriFy automatically scans for suspicious content
   - Red highlights indicate potential fake content

2. **Manual Check**
   - Select any text, right-click
   - Choose "Verify with VeriFy"
   - View detailed analysis results

3. **Keyboard Shortcuts**
   - `Ctrl+Shift+V` - Verify selected content
   - `Ctrl+Shift+S` - Toggle auto-scan
   - `Ctrl+Shift+H` - Toggle highlights

## 🎯 Features

✅ **Text Analysis** - Detect fake news and misleading claims  
✅ **Image Detection** - Identify deepfakes and AI-generated images  
✅ **Video Analysis** - Spot manipulated videos and face swaps  
✅ **Audio Verification** - Detect synthetic voice and audio deepfakes  
✅ **URL Checking** - Verify website credibility and safety  
✅ **Real-time Scanning** - Auto-detect suspicious content as you browse  
✅ **Domain Reputation** - Instant warnings for known fake news sites  
✅ **Statistics Tracking** - Monitor your verification history  

## ⚙️ Configuration

Click the VeriFy icon → **Options** to customize:

- **Auto-Scan Settings** - Enable/disable automatic scanning
- **Detection Sensitivity** - Adjust detection thresholds
- **Highlight Colors** - Customize visual indicators
- **Keyboard Shortcuts** - Configure hotkeys
- **Trusted Domains** - Whitelist reliable sources

## 🔧 Troubleshooting

### Extension Not Loading
- Ensure Developer mode is enabled in `chrome://extensions/`
- Check that you selected the `chrome-extension` folder (not the ZIP file)
- Try disabling and re-enabling the extension

### Icon Not Visible
- Click the puzzle icon (🧩) in Chrome toolbar
- Find VeriFy in the list
- Click the pin icon to keep it visible

### Not Detecting Content
- Check if auto-scan is enabled (click extension icon)
- Refresh the webpage after installing
- Ensure your backend server is running

### API Connection Issues
- Verify your backend server is running on `http://localhost:8000`
- Check browser console for error messages
- Ensure API keys are properly configured

## 🔐 Privacy & Security

- ✅ All analysis happens locally when possible
- ✅ No personal data is collected or stored
- ✅ Open-source code - verify security yourself
- ✅ No tracking or analytics

## 📱 Browser Compatibility

- ✅ **Google Chrome** (v90+)
- ✅ **Microsoft Edge** (v90+)
- ✅ **Brave Browser** (v1.20+)
- ✅ **Opera** (v76+)
- ⚠️ Firefox - Use Firefox Add-on version (separate package)

## 🆘 Support

Need help? 

- 📧 Email: support@verify.com
- 💬 Discord: [Join our community](#)
- 🐛 Report bugs: [GitHub Issues](#)
- 📖 Documentation: [Full Docs](#)

## 🔄 Updates

The extension checks for updates automatically. To manually update:

1. Go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Update" button
4. Reload the extension

## ⭐ Rate Us

Enjoying VeriFy? Please rate us on:
- Chrome Web Store (Coming Soon)
- [GitHub](https://github.com/YOUR_USERNAME/verify) - Give us a ⭐

## 📜 License

MIT License - Free to use and modify

---

**Made with ❤️ by the VeriFy Team**

*Fighting misinformation, one verification at a time.*

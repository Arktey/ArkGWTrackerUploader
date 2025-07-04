# ArkGWTrackerUploader

A tool to automatically collect and upload Epic Seven Guild War defense data.

---

## 📦 How to Use

1. **Extract** all files from the release zip to a folder (keep the folder structure!).
2. **Make sure your preferred emulator is running** and you are logged into Epic Seven.
3. **Navigate to the Guild War page** in the game.  
   _You should be on the following screen before starting the uploader:_

   ![Start Screen](start_screen_example.png)

4. **Run `ArkGWTrackerUploader.exe`** (double-click or run from command line).
5. **Enter your daily upload code** when prompted (must be exactly 12 characters).
6. **Follow the on-screen instructions**.  
   - The tool will automatically detect your emulator
   - Data collection will proceed automatically
   - Press `ESC` at any time to stop

7. **After upload** you can safely close the program.

---

## 🎮 Supported Emulators

The tool automatically detects and supports the following emulators:

- **BlueStacks** (all versions)
- **NoxPlayer** (all versions)
- **LDPlayer** (all versions)
- **MEmu** (all versions)
- **Genymotion** (all versions)
- **Andy** (all versions)

### Emulator Detection

The tool uses multiple methods to detect emulators:
- Process detection (finds running emulator processes)
- Registry scanning (finds ADB ports from emulator settings)
- Automatic port testing (verifies ADB connectivity)

---

## ⚠️ Notes

- **Do not move or rename any folders** (`adb`, `heroData`, `outcome_images`).
- The uploader does **not** require Python or any installation.
- If you have issues connecting to your emulator, try running as administrator.
- Make sure ADB is enabled in your emulator settings.

---

## 📧 Support

For questions or issues, please send me an email at arktey.dev@gmail.com or open an issue on the [GitHub repository](https://github.com/Arktey/ArkGWTrackerUploader). 
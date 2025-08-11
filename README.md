# ArkGWTrackerUploader

A tool to automatically collect and upload Epic Seven Guild War defense data. Available in two versions:

- **ADB Version** (Recommended) - Works with Android emulators via ADB
- **PC Client Version** - Works with Epic Seven PC client using mouse control

The ADB Version is recommended as it does not take control of your mouse, allowing you to use your device while running the script.

The script takes approximately 15 minutes to complete.

---

## 📦 How to Use

### ADB Version (Recommended)
1. **Extract** all files from the `ArkGWTrackerUploader-v1.x.x.zip` to a folder (keep the folder structure!).
2. **Make sure your preferred emulator is running** and you are logged into Epic Seven.
3. **Navigate to the Guild War page** in the game.  
   _You should be on the following screen before starting the uploader:_

   ![Start Screen](start_screen_example.png)

4. **Run `ArkGWTrackerUploader.exe`** (double-click or run from command line).
5. **Enter your daily upload code** when prompted, you can find the code on your account page on the [Ark Guild War Tracker](https://ark-gw-tracker-web.vercel.app) site after logging in (must be exactly 12 characters).
6. **Follow the on-screen instructions**.  
   - The tool will automatically detect your emulator
   - Data collection will proceed automatically
   - Press `ESC` at any time to stop

7. You can safely close the program at any time and continue where you left off when it prompts you to continue.


### PC Client Version
1. **Extract** all files from the `ArkGWTracker_PC-v1.x.x.zip` to a folder (keep the folder structure!).
2. **Make sure Epic Seven PC client is running** and you are logged in.
3. **Navigate to the Guild War page** in the game**.
4. **Run `ArkGWTracker_PC.exe` as Administrator** (required for Windows API access).
5. **Enter your daily upload code** when prompted.
6. **Follow the on-screen instructions**.  
   - The tool will automatically find and manage the Epic Seven window
   - Data collection will proceed automatically using mouse control
   - Press `ESC` at any time to stop

7. You can safely close the program at any time and continue where you left off when it prompts you to continue.


---

## 🎮 Supported Platforms

### ADB Version - Supported Emulators
The ADB version automatically detects and supports the following emulators:

- **BlueStacks** (all versions)
- **NoxPlayer** (all versions)
- **LDPlayer** (all versions)
- **MEmu** (all versions)
- **Genymotion** (all versions)
- **Andy** (all versions)


### PC Client Version - Epic Seven PC Client
- **Epic Seven PC Client** (Windows)


---

## ⚠️ Notes

### ADB Version
- **Do not move or rename any folders** (`adb`, `heroData`, `outcome_images`).
- The uploader does **not** require Python or any installation.
- If you have issues connecting to your emulator, try running as administrator.
- Make sure ADB is enabled in your emulator settings.

### PC Client Version
- **Do not move or rename any folders** (`heroData`, `outcome_images`).
- The uploader does **not** require Python or any installation.
- **Must run as Administrator** for Windows API access.
- **Mouse control** - the tool will move your mouse cursor during operation.
- **Window management** - the tool will resize and position the Epic Seven window if needed.

---

## 📧 Support

For questions or issues, please send me and email arktey.dev@gmail.com or open an issue on the [GitHub repository](https://github.com/Arktey/ArkGWTrackerUploader). 
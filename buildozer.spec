[app]

# (str) Title of your application
title = MusicDL

# (str) Package name
package.name = musicdl

# (str) Package domain (needed for android/ios packaging)
package.domain = org.charlespikachu

# (str) Source code where the main application live
source.dir = .

# (list) Source files to include (let empty to include all files)
source.include_exts = py,png,jpg,kv,atlas,json,ttf,mp3,ogg

# (str) Application versionning
version = 2.11.3

# (list) Application requirements
requirements = python3,kivy,requests,fake-useragent,pycryptodomex,mutagen,click,rich,json-repair,beautifulsoup4,lxml

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible (Android 13+)
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a

# (str) Android entry point, default is 'zlib.py'
#android.entrypoint = zlib.py

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) log level for buildozer (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (bool) Copy libs instead of making a symlink
copy_libs = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug with command output)
log_level = 2

# (bool) Display warning (recommended for most of projects)
warn_on_root = 1
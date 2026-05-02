[app]

title = MusicDL
package.name = musicdl
package.domain = org.musicdl
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,otf,ttf
version = 1.1
requirements = python3,kivy,requests,urllib3,chardet,certifi,idna,beautifulsoup4,lxml,pycryptodome
fullscreen = 0
orientation = portrait
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True
log_level = 2

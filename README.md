# MusicDL Android

MusicDL音乐下载器的Android版本。

## 功能

- 搜索多平台音乐（网易云、酷狗、QQ、咪咕等）
- 下载音乐到本地
- 支持无损音质下载

## 使用GitHub Actions编译APK

### 步骤1: 创建GitHub仓库

1. 登录GitHub
2. 创建新仓库 `musicdl-android`
3. 不要初始化README（本目录已有）

### 步骤2: 设置邮件密码Secret

1. 进入仓库 Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. Name: `EMAIL_PASSWORD`
4. Value: `SZRA8tSrcSg72zAk` (163邮箱授权码)
5. 点击 Add secret

### 步骤3: 上传代码

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/musicdl-android.git
git push -u origin main
```

### 步骤4: 等待编译

上传后GitHub Actions会自动开始编译，约30-60分钟完成。

编译成功后：
- APK会作为Artifacts上传，可在Actions页面下载
- 邮件会自动发送到 13383817575@163.com

### 手动触发编译

在Actions页面点击 "Build Android APK" workflow，点击 "Run workflow"。

## 本地编译（可选）

需要安装：
- JDK 17+
- Android SDK
- buildozer

```bash
pip install buildozer
buildozer android debug
```

## 注意事项

- musicdl仅供学习研究使用，请勿用于商业目的
- 请尊重版权，通过正版渠道获取音乐
- APK仅支持ARM64设备（如华为Mate X5）
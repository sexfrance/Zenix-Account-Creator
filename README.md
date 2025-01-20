<div align="center">
  <h2 align="center">Zenix Account Creator</h2>
  <p align="center">
    An automated tool for creating [Zenix accounts](https://zenix.vast.sh) with Turnstile captcha solver, proxy handling, and multi-threading capabilities.
    <br />
    <br />
    <a href="https://discord.cyberious.xyz">💬 Discord</a>
    ·
    <a href="#-changelog">📜 ChangeLog</a>
    ·
    <a href="https://github.com/sexfrance/Zenix-Account-Creator/issues">⚠️ Report Bug</a>
    ·
    <a href="https://github.com/sexfrance/Zenix-Account-Creator/issues">💡 Request Feature</a>
  </p>
</div>

---

### ⚙️ Installation

- Requires: `Python 3.7+`
- Make a python virtual environment: `python3 -m venv venv`
- Source the environment: `venv\Scripts\activate` (Windows) / `source venv/bin/activate` (macOS, Linux)
- Install the requirements: `pip install -r requirements.txt`

---

### 🔥 Features

- Automated Zenix account creation
- Turnstile captcha solver integration (free!)
- Proxy support for avoiding rate limits
- Multi-threaded account generation
- Real-time creation tracking with console title updates
- Configurable thread count
- Debug mode for troubleshooting
- Proxy/Proxyless mode support
- Custom password support

---

### 📝 Usage

1. **Configuration**:
   Edit `input/config.toml`:

   ```toml
   [data]
   password = "optional_custom_password" # Leave empty for random password generation

   [dev]
   Debug = false
   Proxyless = false
   Threads = 1
   ```

2. **Proxy Setup** (Optional):

   - Add proxies to `input/proxies.txt` (one per line)
   - Format: `ip:port` or `user:pass@ip:port`

3. **Running the script**:

   ```bash
   python main.py
   ```

4. **Output**:
   - Created accounts are saved to `output/accounts.txt`
   - Format: `email:password`

---

### 📹 Preview

![Preview](https://i.imgur.com/6mN5baD.gif)

---

### ❗ Disclaimers

- This project is for educational purposes only
- The author is not responsible for any misuse of this tool
- Use responsibly and in accordance with Zenix's terms of service

---

### 📜 ChangeLog

```diff
v0.0.1 ⋮ 12/26/2024
! Initial release
+ Added Turnstile captcha solver
+ Added multi-threading support
+ Added proxy support
```

<p align="center">
  <img src="https://img.shields.io/github/license/sexfrance/Zenix-Account-Creator.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/stars/sexfrance/Zenix-Account-Creator.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
  <img src="https://img.shields.io/github/languages/top/sexfrance/Zenix-Account-Creator.svg?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA"/>
</p>

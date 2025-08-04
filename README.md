# Telegram C2 Profile for Mythic

A C2 profile that uses the Telegram Bot API for command and control communication. This profile is implemented in Python and provides covert communication channels through Telegram messaging.

## Features

- 🤖 **Telegram Bot Integration**: Uses official Telegram Bot API
- 🔒 **Auto Message Cleanup**: Automatically deletes messages for OPSEC
- 📁 **Large File Support**: Handles large payloads via document uploads  
- ⚡ **Real-time Communication**: gRPC Push C2 protocol for instant messaging
- 🌐 **Proxy Support**: Configure HTTP/HTTPS proxies for network restrictions
- ⏱️ **Configurable Timing**: Adjustable callback intervals and jitter

## How to install

Within Mythic you can run:

```bash
sudo ./mythic-cli install github https://github.com/your-repo/telegram-c2
```

## Quick Setup Guide

### Step 1: Create Telegram Bot

1. Open Telegram and message **@BotFather**
2. Send `/newbot` command
3. Follow instructions to set bot name and username
4. **Copy the Bot Token** provided by BotFather
5. Send `/setprivacy` and select your bot, then select **Disable** to allow bot to read all messages

### Step 2: Create Communication Channel

**Option A: Private Channel (Recommended)**
1. Create a new private channel in Telegram
2. Add your bot as an administrator with permissions to:
   - Send messages
   - Delete messages  
   - Send documents
3. Right-click the channel and copy the channel link
4. The channel ID will be in format: `-100XXXXXXXXX`

**Option B: Private Group**
1. Create a new private group
2. Add your bot to the group
3. Make bot an admin with message permissions
4. Use the group chat ID (negative number)

### Step 3: Get Chat ID

To find your chat/channel ID:

1. Send a test message to your channel/group
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Look for the "chat" object and copy the "id" value
4. Channel IDs are negative numbers (e.g., `-1001234567890`)

### Step 4: Configure C2 Profile in Mythic

1. Navigate to **Mythic UI → C2 Profiles**
2. Find the **telegram** profile and click **Start**
3. Click **View/Edit Config** 
4. Enter your configuration:
   - **telegram_token**: Your bot token from BotFather
   - **chat_id**: Your channel/group ID  
   - **delete_messages**: `T` (recommended for OPSEC)
5. Click **Update Config**
6. Start the profile

## Configuration Parameters

| Parameter | Description | Required | Default | Example |
|-----------|-------------|----------|---------|---------|
| `telegram_token` | Bot token from @BotFather | ✅ | - | `1234567890:ABCD...` |
| `chat_id` | Chat/Channel ID | ✅ | - | `-1001234567890` |
| `callback_interval` | Agent checkin interval (seconds) | ❌ | `60` | `30` |
| `callback_jitter` | Randomization percentage | ❌ | `10` | `15` |
| `delete_messages` | Auto-delete messages | ❌ | `T` | `T` or `F` |
| `user_agent` | HTTP User-Agent | ❌ | Mozilla/5.0... | Custom UA |
| `proxy_host` | Proxy server URL | ❌ | - | `http://proxy.com` |
| `proxy_port` | Proxy port | ❌ | - | `8080` |
| `proxy_user` | Proxy username | ❌ | - | `username` |
| `proxy_pass` | Proxy password | ❌ | - | `password` |

## How It Works

### Architecture
```
Mythic Core ←→ gRPC ←→ Telegram C2 Server ←→ Telegram API ←→ Agent
```

### Message Flow

**From Mythic to Agent:**
1. Operator sends command in Mythic UI
2. Mythic Core forwards command via gRPC to Telegram C2 Server
3. Server formats command as JSON message
4. Message sent to configured Telegram channel
5. Agent monitors channel and processes command

**From Agent to Mythic:**
1. Agent sends response as JSON to Telegram channel
2. Telegram Server receives message via Bot API
3. Message forwarded to Mythic Core via gRPC  
4. Original message deleted from Telegram (if enabled)

### Message Format
```json
{
    "message": "base64_encoded_payload",
    "sender_id": "agent_uuid",
    "to_server": true,
    "client_id": "tracking_id"
}
```

## Security & OPSEC

### ✅ Security Features
- **Automatic Cleanup**: Messages deleted after processing
- **Legitimate Traffic**: Appears as normal Telegram bot activity
- **Document Upload**: Large payloads sent as files (auto-deleted)
- **Private Channels**: Recommend using private channels/groups
- **Proxy Support**: Route traffic through proxies

### 🛡️ OPSEC Recommendations
- Use dedicated Telegram account for bot creation
- Create private channel/group for C2 communications
- Enable 2FA on Telegram account
- Monitor bot activity for suspicious patterns
- Consider operational security of channel names
- Use appropriate callback intervals to avoid detection

## Troubleshooting

### Common Issues

**❌ Bot Not Responding:**
- Verify bot token is correct and not expired
- Ensure bot is added to the specified chat/channel  
- Check bot has necessary permissions (send messages, upload files)
- Confirm `/setprivacy` is disabled for the bot

**❌ Messages Not Being Processed:**
- Confirm chat_id is correct (use /getUpdates to verify)
- Check network connectivity to Telegram API  
- Verify gRPC connection to Mythic Core
- Review server logs for error messages

**❌ Permission Errors:**
- Bot needs admin permissions in channels
- Private groups require bot to be added first
- Check Telegram API rate limits
- Ensure bot can delete messages if cleanup is enabled

### Debug Commands

```bash
# Check Mythic logs
sudo ./mythic-cli logs telegram

# Restart profile
sudo ./mythic-cli telegram restart

# Get bot info
curl "https://api.telegram.org/bot<TOKEN>/getMe"

# Get recent updates  
curl "https://api.telegram.org/bot<TOKEN>/getUpdates"
```

## Development

### Local Testing
1. Copy `config.example.json` to `config.json`
2. Update with your bot token and chat ID
3. Run: `python3 server.py`

### Dependencies
- Python 3.8+
- python-telegram-bot v20.7
- aiofiles
- grpcio
- protobuf

## Support

For issues and questions:
- Create an issue on the GitHub repository
- Check Mythic documentation for C2 profile development
- Review Telegram Bot API documentation

## Credits

Based on the Discord C2 profile architecture by @tr41nwr3ck & @checkymander
Adapted for Telegram by @your_username

# Telegram C2 Profile Documentation

## Overview

The Telegram C2 Profile allows Mythic to use Telegram Bot API as a command and control channel. This profile is implemented in Python and provides a covert communication channel through Telegram messaging.

## Features

- **Telegram Bot Integration**: Uses official Telegram Bot API
- **Message Cleanup**: Automatically deletes messages for OPSEC
- **Large Message Support**: Handles large payloads via document uploads
- **Real-time Communication**: gRPC Push C2 protocol for instant messaging
- **Proxy Support**: Configure HTTP/HTTPS proxies for network restrictions
- **Configurable Timing**: Adjustable callback intervals and jitter

## Architecture

```
Mythic Core ←→ gRPC ←→ Telegram C2 Server ←→ Telegram API ←→ Agent
```

## Message Flow

### From Mythic to Agent:
1. Mythic Core sends command via gRPC
2. Telegram C2 Server receives command
3. Message formatted as JSON and sent to Telegram chat
4. Agent monitors chat and processes command

### From Agent to Mythic:
1. Agent sends response as JSON message to Telegram chat
2. Telegram C2 Server receives message via webhook/polling
3. Message forwarded to Mythic Core via gRPC
4. Original message deleted from Telegram (if configured)

## Message Format

All messages use a standardized JSON format:

```json
{
    "message": "base64_encoded_payload",
    "sender_id": "unique_agent_or_server_id", 
    "to_server": true/false,
    "client_id": "tracking_id"
}
```

- `message`: Base64 encoded command or response data
- `sender_id`: UUID identifying the sender (agent or server)
- `to_server`: Boolean indicating message direction (true = agent→server)
- `client_id`: Tracking ID for correlating requests/responses

## Configuration Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `telegram_token` | Bot token from @BotFather | Yes | - |
| `chat_id` | Chat/Channel ID for communication | Yes | - |
| `callback_interval` | Agent checkin interval (seconds) | No | 60 |
| `callback_jitter` | Randomization percentage | No | 10 |
| `delete_messages` | Auto-delete messages (T/F) | No | T |
| `user_agent` | HTTP User-Agent string | No | Mozilla/5.0... |
| `proxy_host` | Proxy server URL | No | - |
| `proxy_port` | Proxy server port | No | - |
| `proxy_user` | Proxy username | No | - |
| `proxy_pass` | Proxy password | No | - |

## Security Considerations

### OPSEC Features:
- **Automatic Cleanup**: Messages are deleted after processing
- **Legitimate Traffic**: Appears as normal Telegram bot activity
- **Private Channels**: Recommend using private channels/groups
- **Document Upload**: Large payloads sent as files (auto-deleted)

### Recommendations:
- Use dedicated Telegram account for bot creation
- Create private channel/group for C2 communications
- Enable 2FA on Telegram account
- Consider using Telegram's secret chat features
- Monitor bot activity for suspicious patterns

## Troubleshooting

### Common Issues:

**Bot Not Responding:**
- Verify bot token is correct and valid
- Ensure bot is added to the specified chat/channel
- Check bot has necessary permissions (send messages, upload files)

**Messages Not Being Processed:**
- Confirm chat_id is correct (use /getUpdates to verify)
- Check network connectivity to Telegram API
- Verify gRPC connection to Mythic Core

**Permission Errors:**
- Bot needs admin permissions in channels
- Private groups require bot to be added first
- Check Telegram API rate limits

### Debug Mode:
Set `DEBUG=true` environment variable for verbose logging.

## Installation Notes

- Requires Python 3.8+
- Uses `python-telegram-bot` library v20.7
- Includes async/await support for better performance
- Compatible with Mythic's gRPC Push C2 protocol

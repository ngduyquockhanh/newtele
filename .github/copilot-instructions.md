<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Mythic Telegram C2 Profile

This is a Mythic C2 Profile that uses Telegram Bot API for command and control communication.

## Project Structure
- This project is based on the Mythic framework architecture
- Uses Python wrapper for Mythic integration
- Uses C# .NET for Telegram Bot implementation
- Implements gRPC Push C2 protocol for real-time communication
- Uses Telegram Bot API instead of Discord API for covert channels

## Development Guidelines
- Follow Mythic C2 Profile conventions
- Maintain compatibility with Mythic framework
- Use secure communication patterns
- Implement proper error handling and logging
- Follow the existing Discord C2 profile patterns but adapt for Telegram

## Key Components
- `main.py`: Python entry point and C# build process
- `telegram.py`: Python configuration wrapper for Mythic
- `TelegramClient.cs`: Core Telegram Bot implementation
- `MythicClient.cs`: gRPC communication with Mythic core
- `config.json`: Bot token and chat configuration

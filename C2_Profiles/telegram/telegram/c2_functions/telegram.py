from mythic_container.C2ProfileBase import *
from pathlib import Path
import os

class Telegram(C2Profile):
    name = "telegram"
    description = "Telegram Bot API C2 Profile"
    author = "@your_username"
    is_p2p = False
    is_server_routed = False
    server_folder_path = Path(".") / "telegram" / "c2_code"
    server_binary_path = server_folder_path / "server.py"
    
    parameters = [
        C2ProfileParameter(
            name="telegram_token",
            description="Bot Token from @BotFather",
            default_value="",
            required=True,
        ),
        C2ProfileParameter(
            name="chat_id",
            description="Chat ID or Channel ID for communication",
            default_value="",
            required=True,
        ),
        C2ProfileParameter(
            name="message_checks",
            description="Number of attempts to send/receive messages before failure",
            default_value="10",
            required=False,
        ),
        C2ProfileParameter(
            name="time_between_checks",
            description="Time between message checks in seconds",
            default_value="10",
            required=False,
        ),
        C2ProfileParameter(
            name="callback_interval",
            description="Callback Interval in seconds",
            default_value="60",
            verifier_regex="^[0-9]+$",
            required=False,
        ),
        C2ProfileParameter(
            name="callback_jitter",
            description="Callback Jitter in percent",
            default_value="10",
            verifier_regex="^[0-9]+$",
            required=False,
        ),
        C2ProfileParameter(
            name="encrypted_exchange_check",
            description="Perform Key Exchange",
            choices=["T", "F"],
            parameter_type=ParameterType.ChooseOne,
            required=False,
        ),
        C2ProfileParameter(
            name="AESPSK",
            description="Crypto type",
            default_value="aes256_hmac",
            parameter_type=ParameterType.ChooseOne,
            choices=["aes256_hmac", "none"],
            required=False,
            crypto_type=True
        ),
        C2ProfileParameter(
            name="user_agent",
            description="User Agent for HTTP requests",
            default_value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            required=False,
        ),
        C2ProfileParameter(
            name="proxy_host",
            description="Proxy Host",
            default_value="",
            required=False,
            verifier_regex="^$|^(http|https):\/\/[a-zA-Z0-9]+",
        ),
        C2ProfileParameter(
            name="proxy_port",
            description="Proxy Port",
            default_value="",
            verifier_regex="^$|^[0-9]+$",
            required=False,
        ),
        C2ProfileParameter(
            name="proxy_user",
            description="Proxy Username",
            default_value="",
            required=False,
        ),
        C2ProfileParameter(
            name="proxy_pass",
            description="Proxy Password",
            default_value="",
            required=False,
        ),
        C2ProfileParameter(
            name="killdate",
            description="Kill Date",
            parameter_type=ParameterType.Date,
            default_value=365,
            required=False,
        ),
        C2ProfileParameter(
            name="delete_messages",
            description="Auto-delete messages for OPSEC",
            choices=["T", "F"],
            parameter_type=ParameterType.ChooseOne,
            default_value="T",
            required=False,
        ),
    ]

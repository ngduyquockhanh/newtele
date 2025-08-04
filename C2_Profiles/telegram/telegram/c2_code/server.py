#!/usr/bin/env python3

import asyncio
import json
import logging
import os
import sys
import base64
import uuid
from pathlib import Path
from typing import Optional
import aiofiles

# Telegram Bot API
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters
from telegram.constants import ParseMode

# gRPC and Mythic
import grpc
from concurrent.futures import ThreadPoolExecutor
import threading
import queue

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MythicMessageWrapper:
    """Message wrapper for Mythic communication"""
    def __init__(self, message: str = "", sender_id: str = "", to_server: bool = False, client_id: str = ""):
        self.message = message
        self.sender_id = sender_id
        self.to_server = to_server
        self.client_id = client_id
    
    def to_dict(self):
        return {
            "message": self.message,
            "sender_id": self.sender_id,
            "to_server": self.to_server,
            "client_id": self.client_id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            message=data.get("message", ""),
            sender_id=data.get("sender_id", ""),
            to_server=data.get("to_server", False),
            client_id=data.get("client_id", "")
        )

class TelegramMythicClient:
    """Handles communication with Mythic core via gRPC"""
    
    def __init__(self, telegram_client):
        self.telegram_client = telegram_client
        self.uuid = str(uuid.uuid4())
        self.mythic_channel = None
        self.mythic_connection = None
        self.mythic_connector = None
        self.message_queue = queue.Queue()
        self.running = False
        
    async def connect_to_mythic(self):
        """Connect to Mythic gRPC server"""
        try:
            # Use localhost for production, adjust for debug
            mythic_address = "127.0.0.1:17444"
            if os.getenv("DEBUG") == "true":
                mythic_address = "10.30.26.108:17444"
            
            # Note: This is a placeholder for gRPC implementation
            # You'll need to implement the actual gRPC client based on pushC2GRPC.proto
            logger.info(f"Connecting to Mythic at {mythic_address}")
            
            # For now, we'll simulate the connection
            self.running = True
            logger.info("Connected to Mythic successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to Mythic: {e}")
            
    async def send_to_mythic(self, sender_id: str, message: str):
        """Send message from agent to Mythic"""
        try:
            logger.info(f"Sending to Mythic from {sender_id}")
            # This would use gRPC to send PushC2MessageFromAgent
            # For now, just log the message
            logger.debug(f"Message: {message[:100]}...")
            
        except Exception as e:
            logger.error(f"Error sending to Mythic: {e}")
    
    async def receive_from_mythic(self):
        """Receive messages from Mythic and forward to Telegram"""
        while self.running:
            try:
                # This would listen for PushC2MessageFromMythic via gRPC
                # For now, we'll simulate by checking a queue
                await asyncio.sleep(1)
                
                if not self.message_queue.empty():
                    message_data = self.message_queue.get()
                    await self.telegram_client.send_to_telegram(
                        message_data["message"], 
                        message_data["tracking_id"]
                    )
                    
            except Exception as e:
                logger.error(f"Error receiving from Mythic: {e}")
                await asyncio.sleep(5)

class TelegramC2Server:
    """Main Telegram C2 Server class"""
    
    def __init__(self):
        self.config = self.load_config()
        self.bot = None
        self.application = None
        self.mythic_client = None
        self.chat_id = None
        self.delete_messages = True
        
    def load_config(self) -> dict:
        """Load configuration from config.json"""
        config_path = Path("config.json")
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                logger.info("Configuration loaded successfully")
                return config
        except FileNotFoundError:
            logger.error("config.json not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config.json: {e}")
            sys.exit(1)
    
    async def initialize(self):
        """Initialize Telegram bot and Mythic client"""
        try:
            # Get configuration
            token = self.config.get("telegram_token", "")
            self.chat_id = self.config.get("chat_id", "")
            self.delete_messages = self.config.get("delete_messages", "T") == "T"
            
            if not token or not self.chat_id:
                logger.error("telegram_token and chat_id are required in config.json")
                sys.exit(1)
            
            # Initialize Telegram bot
            self.application = Application.builder().token(token).build()
            self.bot = self.application.bot
            
            # Add message handler
            self.application.add_handler(
                MessageHandler(filters.ALL, self.handle_telegram_message)
            )
            
            # Initialize Mythic client
            self.mythic_client = TelegramMythicClient(self)
            await self.mythic_client.connect_to_mythic()
            
            logger.info("Telegram C2 Server initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            sys.exit(1)
    
    async def handle_telegram_message(self, update: Update, context):
        """Handle incoming Telegram messages"""
        try:
            message = update.message
            if not message or not message.text:
                return
            
            # Check if message is from our monitored chat
            if str(message.chat_id) != str(self.chat_id):
                return
            
            # Try to parse as Mythic message
            try:
                data = json.loads(message.text)
                mythic_message = MythicMessageWrapper.from_dict(data)
                
                # Check if this is a message to the server (from agent)
                if mythic_message.to_server:
                    logger.info(f"Received message from agent {mythic_message.sender_id}")
                    
                    # Delete message for OPSEC if enabled
                    if self.delete_messages:
                        try:
                            await message.delete()
                        except Exception as e:
                            logger.warning(f"Could not delete message: {e}")
                    
                    # Forward to Mythic
                    await self.mythic_client.send_to_mythic(
                        mythic_message.sender_id,
                        mythic_message.message
                    )
                    
            except json.JSONDecodeError:
                # Not a JSON message, ignore
                pass
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                
        except Exception as e:
            logger.error(f"Error in handle_telegram_message: {e}")
    
    async def send_to_telegram(self, message: str, tracking_id: str):
        """Send message from Mythic to Telegram"""
        try:
            mythic_message = MythicMessageWrapper(
                message=message,
                sender_id=self.mythic_client.uuid,
                to_server=False,
                client_id=tracking_id
            )
            
            message_text = json.dumps(mythic_message.to_dict())
            
            # Check message length (Telegram limit is 4096 characters)
            if len(message_text) > 4000:
                # Send as document
                await self.send_as_document(message_text, tracking_id)
            else:
                # Send as text message
                await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message_text,
                    parse_mode=ParseMode.HTML
                )
            
            logger.info(f"Sent message to Telegram (tracking: {tracking_id})")
            
        except Exception as e:
            logger.error(f"Error sending to Telegram: {e}")
    
    async def send_as_document(self, message_text: str, filename: str):
        """Send large message as document"""
        try:
            # Create temporary file
            temp_file = f"/tmp/{filename}.txt"
            
            async with aiofiles.open(temp_file, 'w') as f:
                await f.write(message_text)
            
            # Send as document
            with open(temp_file, 'rb') as f:
                await self.bot.send_document(
                    chat_id=self.chat_id,
                    document=f,
                    filename=f"{filename}.txt"
                )
            
            # Clean up
            os.remove(temp_file)
            
        except Exception as e:
            logger.error(f"Error sending document: {e}")
    
    async def catch_up_messages(self):
        """Process any missed messages on startup"""
        try:
            # Get recent messages from the chat
            updates = await self.bot.get_updates(limit=100)
            
            for update in updates:
                if update.message and str(update.message.chat_id) == str(self.chat_id):
                    await self.handle_telegram_message(update, None)
            
            logger.info("Catch-up completed")
            
        except Exception as e:
            logger.error(f"Error during catch-up: {e}")
    
    async def start(self):
        """Start the Telegram C2 server"""
        try:
            await self.initialize()
            
            # Start Mythic receiver task
            asyncio.create_task(self.mythic_client.receive_from_mythic())
            
            # Catch up on missed messages
            await self.catch_up_messages()
            
            # Start Telegram bot
            logger.info("Starting Telegram C2 Server...")
            await self.application.initialize()
            await self.application.start()
            
            # Keep running
            await self.application.updater.start_polling()
            
            # Keep the application running
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        except Exception as e:
            logger.error(f"Error in start: {e}")
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Gracefully shutdown the server"""
        try:
            if self.mythic_client:
                self.mythic_client.running = False
            
            if self.application:
                await self.application.stop()
                await self.application.shutdown()
            
            logger.info("Telegram C2 Server shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

async def main():
    """Main entry point"""
    server = TelegramC2Server()
    await server.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server crashed: {e}")
        sys.exit(1)

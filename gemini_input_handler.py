#!/usr/bin/env python3
"""
Gemini CLI Input Handler - " telefon central" for Gemini CLI calls
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any

class GeminiInputHandler:
    def __init__(self):
        self.message_queue = []
        self.windsurf_integration = True
        
    async def handle_gemini_message(self, message_data: Dict[str, Any]):
        """Handle incoming message from Gemini CLI"""
        try:
            print(f"[Gemini Phone] Ring ring! Message from Gemini CLI: {message_data.get('type', 'unknown')}")
            
            # Store message
            message_entry = {
                "id": f"gemini_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": message_data.get("type", "message"),
                "content": message_data.get("content", ""),
                "timestamp": datetime.now().isoformat(),
                "priority": message_data.get("priority", "normal"),
                "action_required": message_data.get("action_required", False)
            }
            
            self.message_queue.append(message_entry)
            
            # Display in Windsurf
            await self.display_in_windsurf(message_entry)
            
            # Save to log
            await self.save_message_log(message_entry)
            
            return {"status": "received", "message_id": message_entry["id"]}
            
        except Exception as e:
            print(f"[Gemini Phone] Error handling message: {e}")
            return {"status": "error", "error": str(e)}
    
    async def handle_gemini_review(self, review_data: Dict[str, Any]):
        """Handle code review from Gemini CLI"""
        try:
            print(f"[Gemini Phone] Code review received!")
            
            review_entry = {
                "id": f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": "code_review",
                "file": review_data.get("file", ""),
                "review": review_data.get("review", ""),
                "suggestions": review_data.get("suggestions", []),
                "timestamp": datetime.now().isoformat(),
                "priority": "high"
            }
            
            self.message_queue.append(review_entry)
            
            # Special display for reviews
            await self.display_review_in_windsurf(review_entry)
            
            return {"status": "review_received", "review_id": review_entry["id"]}
            
        except Exception as e:
            print(f"[Gemini Phone] Error handling review: {e}")
            return {"status": "error", "error": str(e)}
    
    async def handle_gemini_suggestion(self, suggestion_data: Dict[str, Any]):
        """Handle suggestions from Gemini CLI"""
        try:
            print(f"[Gemini Phone] Suggestion received!")
            
            suggestion_entry = {
                "id": f"suggestion_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": "suggestion", 
                "context": suggestion_data.get("context", ""),
                "suggestion": suggestion_data.get("suggestion", ""),
                "confidence": suggestion_data.get("confidence", 0.8),
                "timestamp": datetime.now().isoformat()
            }
            
            self.message_queue.append(suggestion_entry)
            
            # Display suggestion
            await self.display_suggestion_in_windsurf(suggestion_entry)
            
            return {"status": "suggestion_received", "suggestion_id": suggestion_entry["id"]}
            
        except Exception as e:
            print(f"[Gemini Phone] Error handling suggestion: {e}")
            return {"status": "error", "error": str(e)}
    
    async def display_in_windsurf(self, message_entry: Dict[str, Any]):
        """Display message in Windsurf interface"""
        try:
            # Create notification file for Windsurf to pick up
            notification_file = f"d:/Gemini/agent-hand/bridge/windsurf_notifications/{message_entry['id']}.json"
            os.makedirs("d:/Gemini/agent-hand/bridge/windsurf_notifications", exist_ok=True)
            
            notification_data = {
                "type": "gemini_message",
                "title": f"Gemini CLI - {message_entry['type'].title()}",
                "content": message_entry["content"],
                "priority": message_entry["priority"],
                "timestamp": message_entry["timestamp"],
                "action_required": message_entry["action_required"]
            }
            
            with open(notification_file, "w", encoding="utf-8") as f:
                json.dump(notification_data, f, indent=2, ensure_ascii=False)
            
            print(f"[Gemini Phone] Message displayed in Windsurf: {notification_file}")
            
        except Exception as e:
            print(f"[Gemini Phone] Failed to display in Windsurf: {e}")
    
    async def display_review_in_windsurf(self, review_entry: Dict[str, Any]):
        """Display code review in Windsurf"""
        try:
            notification_file = f"d:/Gemini/agent-hand/bridge/windsurf_notifications/{review_entry['id']}.json"
            os.makedirs("d:/Gemini/agent-hand/bridge/windsurf_notifications", exist_ok=True)
            
            notification_data = {
                "type": "code_review",
                "title": f"Code Review - {review_entry['file']}",
                "content": review_entry["review"],
                "suggestions": review_entry["suggestions"],
                "priority": "high",
                "timestamp": review_entry["timestamp"],
                "file": review_entry["file"]
            }
            
            with open(notification_file, "w", encoding="utf-8") as f:
                json.dump(notification_data, f, indent=2, ensure_ascii=False)
            
            print(f"[Gemini Phone] Review displayed in Windsurf: {notification_file}")
            
        except Exception as e:
            print(f"[Gemini Phone] Failed to display review in Windsurf: {e}")
    
    async def display_suggestion_in_windsurf(self, suggestion_entry: Dict[str, Any]):
        """Display suggestion in Windsurf"""
        try:
            notification_file = f"d:/Gemini/agent-hand/bridge/windsurf_notifications/{suggestion_entry['id']}.json"
            os.makedirs("d:/Gemini/agent-hand/bridge/windsurf_notifications", exist_ok=True)
            
            notification_data = {
                "type": "suggestion",
                "title": f"Suggestion - {suggestion_entry['context']}",
                "content": suggestion_entry["suggestion"],
                "confidence": suggestion_entry["confidence"],
                "timestamp": suggestion_entry["timestamp"]
            }
            
            with open(notification_file, "w", encoding="utf-8") as f:
                json.dump(notification_data, f, indent=2, ensure_ascii=False)
            
            print(f"[Gemini Phone] Suggestion displayed in Windsurf: {notification_file}")
            
        except Exception as e:
            print(f"[Gemini Phone] Failed to display suggestion in Windsurf: {e}")
    
    async def save_message_log(self, message_entry: Dict[str, Any]):
        """Save message to log file"""
        try:
            log_file = "d:/Gemini/agent-hand/bridge/logs/gemini_messages.log"
            os.makedirs("d:/Gemini/agent-hand/bridge/logs", exist_ok=True)
            
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"{datetime.now().isoformat()} - {message_entry['type']} - {message_entry['id']}\n")
                f.write(f"Content: {message_entry.get('content', '')}\n")
                f.write("-" * 50 + "\n")
            
        except Exception as e:
            print(f"[Gemini Phone] Failed to save message log: {e}")

# Global instance
gemini_input_handler = GeminiInputHandler()

async def handle_gemini_message(message_data: Dict[str, Any]):
    """Export function for server integration"""
    return await gemini_input_handler.handle_gemini_message(message_data)

async def handle_gemini_review(review_data: Dict[str, Any]):
    """Export function for server integration"""
    return await gemini_input_handler.handle_gemini_review(review_data)

async def handle_gemini_suggestion(suggestion_data: Dict[str, Any]):
    """Export function for server integration"""
    return await gemini_input_handler.handle_gemini_suggestion(suggestion_data)

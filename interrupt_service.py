from typing import Dict, Optional, List
from datetime import datetime
from memory_service import memory_service

class InterruptService:
    def __init__(self):
        self.active_interruptions: Dict[str, Dict] = {}
    
    async def handle_voice_interruption(self, session_id: str, agent_id: str, 
                                      interrupted_content: str, user_input: str) -> Dict:
        """Handle voice-triggered interruption"""
        interrupt_data = {
            "type": "voice",
            "timestamp": int(datetime.now().timestamp() * 1000),
            "agent_id": agent_id,
            "interrupted_content": interrupted_content,
            "user_input": user_input,
            "session_id": session_id
        }
        
        # Store interruption data
        self.active_interruptions[f"{session_id}_{agent_id}"] = interrupt_data
        
        # Update memory with interruption
        memory_service.handle_interruption(session_id, interrupted_content)
        
        # Add user message that caused interruption
        memory_service.add_message(session_id, "user", user_input, "asr")
        
        return {
            "status": "interrupted",
            "type": "voice",
            "timestamp": interrupt_data["timestamp"],
            "session_id": session_id
        }
    
    async def handle_manual_interruption(self, session_id: str, agent_id: str, 
                                       interrupted_content: Optional[str] = None) -> Dict:
        """Handle manual interruption (button/command)"""
        interrupt_data = {
            "type": "manual",
            "timestamp": int(datetime.now().timestamp() * 1000),
            "agent_id": agent_id,
            "interrupted_content": interrupted_content or "",
            "session_id": session_id
        }
        
        # Store interruption data
        self.active_interruptions[f"{session_id}_{agent_id}"] = interrupt_data
        
        # Update memory if there was content being spoken
        if interrupted_content:
            memory_service.handle_interruption(session_id, interrupted_content)
        
        return {
            "status": "interrupted",
            "type": "manual", 
            "timestamp": interrupt_data["timestamp"],
            "session_id": session_id
        }
    
    def get_interruption_config(self, interrupt_mode: str = "interrupt", 
                              duration_ms: int = 500) -> Dict:
        """Get interruption configuration for agent"""
        return {
            "advanced_features": {
                "enable_aivad": True,  # Enable AI Voice Activity Detection
                "enable_rtm": True     # Enable Real-time Messaging
            },
            "turn_detection": {
                "interrupt_mode": interrupt_mode,  # interrupt, append, ignore
                "interrupt_duration_ms": duration_ms
            }
        }
    
    def clear_interruption(self, session_id: str, agent_id: str):
        """Clear interruption data"""
        key = f"{session_id}_{agent_id}"
        if key in self.active_interruptions:
            del self.active_interruptions[key]
    
    def get_interruption_status(self, session_id: str, agent_id: str) -> Optional[Dict]:
        """Get current interruption status"""
        key = f"{session_id}_{agent_id}"
        return self.active_interruptions.get(key)

interrupt_service = InterruptService()

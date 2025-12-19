from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from datetime import datetime
import json

class MessageMetadata(BaseModel):
    source: str  # asr, message, command, llm, greeting, llm_failure, silence
    user: Optional[str] = None
    interrupted: Optional[bool] = None
    interrupt_timestamp: Optional[int] = None
    original: Optional[str] = None

class MemoryMessage(BaseModel):
    role: str  # user, assistant
    content: str
    turn_id: int
    timestamp: int
    metadata: MessageMetadata

class ShortTermMemory(BaseModel):
    contents: List[MemoryMessage]
    turn_id: int = 0
    timestamp: int
    interruptable: bool = True

class MemoryService:
    def __init__(self):
        self.sessions: Dict[str, ShortTermMemory] = {}
    
    def create_session(self, session_id: str) -> ShortTermMemory:
        """Create new memory session"""
        memory = ShortTermMemory(
            contents=[],
            turn_id=0,
            timestamp=int(datetime.now().timestamp() * 1000),
            interruptable=True
        )
        self.sessions[session_id] = memory
        return memory
    
    def add_message(self, session_id: str, role: str, content: str, 
                   source: str, user: Optional[str] = None) -> MemoryMessage:
        """Add message to session memory"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        memory = self.sessions[session_id]
        
        # Increment turn_id for new user messages
        if role == "user":
            memory.turn_id += 1
        
        message = MemoryMessage(
            role=role,
            content=content,
            turn_id=memory.turn_id,
            timestamp=int(datetime.now().timestamp() * 1000),
            metadata=MessageMetadata(source=source, user=user)
        )
        
        memory.contents.append(message)
        memory.timestamp = message.timestamp
        
        return message
    
    def handle_interruption(self, session_id: str, original_content: str) -> Optional[MemoryMessage]:
        """Handle agent message interruption"""
        if session_id not in self.sessions:
            return None
        
        memory = self.sessions[session_id]
        
        # Find last assistant message
        for message in reversed(memory.contents):
            if message.role == "assistant":
                message.metadata.interrupted = True
                message.metadata.interrupt_timestamp = int(datetime.now().timestamp() * 1000)
                message.metadata.original = original_content
                return message
        
        return None
    
    def get_openai_format(self, session_id: str, include_metadata: bool = False) -> List[Dict]:
        """Get memory in OpenAI format"""
        if session_id not in self.sessions:
            return []
        
        memory = self.sessions[session_id]
        messages = []
        
        for msg in memory.contents:
            message_dict = {
                "role": msg.role,
                "content": msg.content
            }
            
            if include_metadata:
                message_dict.update({
                    "turn_id": msg.turn_id,
                    "timestamp": msg.timestamp,
                    "metadata": msg.metadata.model_dump(exclude_none=True)
                })
            
            messages.append(message_dict)
        
        return messages
    
    def get_full_memory(self, session_id: str) -> Optional[ShortTermMemory]:
        """Get complete memory with all fields"""
        return self.sessions.get(session_id)
    
    def summarize_memory(self, session_id: str) -> str:
        """Create summary for long-term storage"""
        if session_id not in self.sessions:
            return ""
        
        memory = self.sessions[session_id]
        
        # Simple summarization - in production use LLM
        topics = []
        for msg in memory.contents:
            if msg.role == "user" and len(msg.content) > 10:
                topics.append(msg.content[:50])
        
        if topics:
            return f"User discussed: {'; '.join(topics[:3])}"
        return "Brief conversation session"
    
    def inject_long_term_memory(self, session_id: str, summary: str) -> List[Dict]:
        """Inject long-term memory as system messages"""
        system_messages = [
            {
                "role": "system",
                "content": "You are an AI interviewer conducting a professional job interview."
            }
        ]
        
        if summary:
            system_messages.append({
                "role": "system", 
                "content": f"Previous conversation context: {summary}"
            })
        
        return system_messages
    
    def clear_session(self, session_id: str):
        """Clear session memory"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def export_session(self, session_id: str) -> Optional[Dict]:
        """Export session for storage"""
        memory = self.get_full_memory(session_id)
        return memory.model_dump() if memory else None

memory_service = MemoryService()

#!/usr/bin/env python3
"""Test Short-term Memory functionality"""

import asyncio
import httpx
import json

async def test_memory_management():
    print("Testing Short-term Memory Management")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    session_id = "test_session_123"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test 1: Add user message
        print("1. Adding user message...")
        response = await client.post(
            f"{base_url}/api/memory/{session_id}/message",
            params={
                "role": "user",
                "content": "Hello, I'm ready for the interview",
                "source": "asr",
                "user": "candidate_123"
            }
        )
        if response.status_code == 200:
            print("✓ User message added")
        else:
            print(f"✗ Failed: {response.status_code}")
        
        # Test 2: Add assistant message
        print("\n2. Adding assistant message...")
        response = await client.post(
            f"{base_url}/api/memory/{session_id}/message",
            params={
                "role": "assistant",
                "content": "Great! Let's start with your background. Can you tell me about your experience?",
                "source": "llm"
            }
        )
        if response.status_code == 200:
            print("✓ Assistant message added")
        else:
            print(f"✗ Failed: {response.status_code}")
        
        # Test 3: Handle interruption
        print("\n3. Testing interruption handling...")
        response = await client.post(
            f"{base_url}/api/memory/{session_id}/interrupt",
            params={
                "original_content": "Great! Let's start with your background. Can you tell me about your experience with Python programming and web development?"
            }
        )
        if response.status_code == 200:
            result = response.json()
            print("✓ Interruption handled")
            if result.get("metadata", {}).get("interrupted"):
                print("  - Message marked as interrupted")
                print(f"  - Original content preserved: {len(result.get('metadata', {}).get('original', ''))} chars")
        else:
            print(f"✗ Failed: {response.status_code}")
        
        # Test 4: Get memory in OpenAI format
        print("\n4. Getting memory in OpenAI format...")
        response = await client.get(f"{base_url}/api/memory/{session_id}?format=openai")
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])
            print(f"✓ Retrieved {len(messages)} messages in OpenAI format")
            for i, msg in enumerate(messages):
                print(f"  {i+1}. {msg['role']}: {msg['content'][:50]}...")
        else:
            print(f"✗ Failed: {response.status_code}")
        
        # Test 5: Get memory with metadata
        print("\n5. Getting memory with extended metadata...")
        response = await client.get(f"{base_url}/api/memory/{session_id}?format=extended")
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])
            print(f"✓ Retrieved {len(messages)} messages with metadata")
            for msg in messages:
                if "metadata" in msg:
                    metadata = msg["metadata"]
                    print(f"  - {msg['role']} (turn {msg.get('turn_id')}, source: {metadata.get('source')})")
                    if metadata.get("interrupted"):
                        print(f"    * Interrupted at {metadata.get('interrupt_timestamp')}")
        else:
            print(f"✗ Failed: {response.status_code}")
        
        # Test 6: Get full memory structure
        print("\n6. Getting full memory structure...")
        response = await client.get(f"{base_url}/api/memory/{session_id}?format=full")
        if response.status_code == 200:
            data = response.json()
            print("✓ Retrieved full memory structure")
            print(f"  - Turn ID: {data.get('turn_id')}")
            print(f"  - Timestamp: {data.get('timestamp')}")
            print(f"  - Interruptable: {data.get('interruptable')}")
            print(f"  - Contents: {len(data.get('contents', []))} messages")
        else:
            print(f"✗ Failed: {response.status_code}")
        
        # Test 7: Get memory summary
        print("\n7. Getting memory summary...")
        response = await client.get(f"{base_url}/api/memory/{session_id}/summary")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Memory summary: {data.get('summary')}")
        else:
            print(f"✗ Failed: {response.status_code}")
        
        # Test 8: Clear memory
        print("\n8. Clearing memory...")
        response = await client.delete(f"{base_url}/api/memory/{session_id}")
        if response.status_code == 200:
            print("✓ Memory cleared")
        else:
            print(f"✗ Failed: {response.status_code}")

async def test_agora_memory_integration():
    print("\nTesting Agora Memory Integration")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    agent_id = "test_agent_123"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test agent history endpoint (will fail without real agent)
        print("1. Testing agent history retrieval...")
        response = await client.get(f"{base_url}/api/agora/agents/{agent_id}/history")
        if response.status_code == 404:
            print("✓ Agent history endpoint working (agent not found as expected)")
        else:
            print(f"? Unexpected response: {response.status_code}")
        
        # Test memory update endpoint
        print("\n2. Testing agent memory update...")
        system_messages = [
            {
                "role": "system",
                "content": "You are an AI interviewer. Previous context: User discussed Python experience."
            }
        ]
        response = await client.patch(
            f"{base_url}/api/agora/agents/{agent_id}/memory",
            json=system_messages
        )
        if response.status_code == 400:
            print("✓ Agent memory update endpoint working (agent not found as expected)")
        else:
            print(f"? Unexpected response: {response.status_code}")

async def main():
    print("Short-term Memory Service Test")
    print("=" * 60)
    
    await test_memory_management()
    await test_agora_memory_integration()
    
    print("\n" + "=" * 60)
    print("Memory test completed!")

if __name__ == "__main__":
    asyncio.run(main())

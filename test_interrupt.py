#!/usr/bin/env python3
"""Test Agent Interruption functionality"""

import asyncio
import httpx
import json

async def test_interrupt_configuration():
    print("Testing Interrupt Configuration")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test 1: Get default interrupt config
        print("1. Getting default interrupt configuration...")
        response = await client.get(f"{base_url}/api/interrupt/config")
        if response.status_code == 200:
            config = response.json()
            print("✓ Default configuration retrieved")
            print(f"  - AIVAD enabled: {config['advanced_features']['enable_aivad']}")
            print(f"  - RTM enabled: {config['advanced_features']['enable_rtm']}")
            print(f"  - Interrupt mode: {config['turn_detection']['interrupt_mode']}")
            print(f"  - Duration: {config['turn_detection']['interrupt_duration_ms']}ms")
        else:
            print(f"✗ Failed: {response.status_code}")
        
        # Test 2: Get custom interrupt config
        print("\n2. Getting custom interrupt configuration...")
        response = await client.get(
            f"{base_url}/api/interrupt/config",
            params={"interrupt_mode": "append", "duration_ms": 1000}
        )
        if response.status_code == 200:
            config = response.json()
            print("✓ Custom configuration retrieved")
            print(f"  - Interrupt mode: {config['turn_detection']['interrupt_mode']}")
            print(f"  - Duration: {config['turn_detection']['interrupt_duration_ms']}ms")
        else:
            print(f"✗ Failed: {response.status_code}")

async def test_voice_interruption():
    print("\nTesting Voice Interruption")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    session_id = "test_session_voice"
    agent_id = "test_agent_123"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test voice interruption
        print("1. Simulating voice interruption...")
        response = await client.post(
            f"{base_url}/api/interrupt/{session_id}/voice",
            params={
                "agent_id": agent_id,
                "interrupted_content": "I was about to explain the technical requirements for this position, including Python programming and...",
                "user_input": "Actually, can you tell me about the company culture instead?"
            }
        )
        if response.status_code == 200:
            result = response.json()
            print("✓ Voice interruption handled")
            print(f"  - Type: {result['type']}")
            print(f"  - Status: {result['status']}")
            print(f"  - Timestamp: {result['timestamp']}")
        else:
            print(f"✗ Failed: {response.status_code}")
        
        # Check interruption status
        print("\n2. Checking interruption status...")
        response = await client.get(
            f"{base_url}/api/interrupt/{session_id}/status",
            params={"agent_id": agent_id}
        )
        if response.status_code == 200:
            status = response.json()
            print("✓ Interruption status retrieved")
            if status.get("type"):
                print(f"  - Type: {status['type']}")
                print(f"  - Agent ID: {status['agent_id']}")
                print(f"  - User input: {status.get('user_input', 'N/A')[:50]}...")
        else:
            print(f"✗ Failed: {response.status_code}")

async def test_manual_interruption():
    print("\nTesting Manual Interruption")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    session_id = "test_session_manual"
    agent_id = "test_agent_456"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test manual interruption
        print("1. Simulating manual interruption...")
        response = await client.post(
            f"{base_url}/api/interrupt/{session_id}/manual",
            params={
                "agent_id": agent_id,
                "interrupted_content": "Let me walk you through our interview process step by step..."
            }
        )
        if response.status_code == 200:
            result = response.json()
            print("✓ Manual interruption handled")
            print(f"  - Type: {result['type']}")
            print(f"  - Status: {result['status']}")
        else:
            print(f"✗ Failed: {response.status_code}")
        
        # Test manual interruption without content
        print("\n2. Simulating manual interruption (no content)...")
        response = await client.post(
            f"{base_url}/api/interrupt/{session_id}/manual",
            params={"agent_id": agent_id}
        )
        if response.status_code == 200:
            result = response.json()
            print("✓ Manual interruption (no content) handled")
        else:
            print(f"✗ Failed: {response.status_code}")

async def test_agora_interrupt_api():
    print("\nTesting Agora Interrupt API")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    agent_id = "test_agent_789"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test Agora interrupt endpoint (will fail without real agent)
        print("1. Testing Agora agent interrupt...")
        response = await client.post(f"{base_url}/api/agora/agents/{agent_id}/interrupt")
        if response.status_code == 400:
            print("✓ Agora interrupt endpoint working (agent not found as expected)")
        else:
            print(f"? Unexpected response: {response.status_code}")

async def test_memory_integration():
    print("\nTesting Memory Integration with Interrupts")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    session_id = "test_session_memory"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Add initial assistant message
        print("1. Adding assistant message...")
        await client.post(
            f"{base_url}/api/memory/{session_id}/message",
            params={
                "role": "assistant",
                "content": "Let me explain the technical requirements...",
                "source": "llm"
            }
        )
        
        # Simulate voice interruption
        print("2. Simulating voice interruption with memory update...")
        await client.post(
            f"{base_url}/api/interrupt/{session_id}/voice",
            params={
                "agent_id": "test_agent",
                "interrupted_content": "Let me explain the technical requirements for this position in detail...",
                "user_input": "Can we skip to salary discussion?"
            }
        )
        
        # Check memory state
        print("3. Checking memory after interruption...")
        response = await client.get(f"{base_url}/api/memory/{session_id}?format=extended")
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])
            print(f"✓ Memory contains {len(messages)} messages")
            
            # Look for interrupted message
            for msg in messages:
                if msg.get("metadata", {}).get("interrupted"):
                    print("  - Found interrupted message:")
                    print(f"    * Original: {msg['metadata']['original'][:50]}...")
                    print(f"    * Displayed: {msg['content'][:50]}...")
                    break
        else:
            print(f"✗ Failed to retrieve memory: {response.status_code}")

async def main():
    print("Agent Interruption Service Test")
    print("=" * 60)
    
    await test_interrupt_configuration()
    await test_voice_interruption()
    await test_manual_interruption()
    await test_agora_interrupt_api()
    await test_memory_integration()
    
    print("\n" + "=" * 60)
    print("Interrupt test completed!")

if __name__ == "__main__":
    asyncio.run(main())

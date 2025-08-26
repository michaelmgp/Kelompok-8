#!/usr/bin/env python3
"""
Generate a unique agent seed for uAgents
Run this once to get a unique seed for your agent
"""

from uagents import Agent
import secrets

def generate_unique_seed():
    """Generate a unique 32-byte seed"""
    # Generate a random 32-byte seed
    seed_bytes = secrets.token_bytes(32)
    seed_hex = seed_bytes.hex()
    
    # Create a temporary agent to get the address
    temp_agent = Agent(name="temp", seed=seed_hex)
    
    print("🔐 Generated Unique Agent Seed:")
    print(f"AGENT_SEED={seed_hex}")
    print(f"AGENT_ADDRESS={temp_agent.address}")
    print("\n⚠️  IMPORTANT:")
    print("- Keep this seed SECRET!")
    print("- Don't share it publicly")
    print("- Use it in your .env file")
    print("- This seed is unique to you"
    
    return seed_hex

if __name__ == "__main__":
    generate_unique_seed()


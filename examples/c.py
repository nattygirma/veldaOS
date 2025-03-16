import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from veldaos.core import VeldaOS
import asyncio

OPENAI_API_KEY = "APIKEY"

async def main():
    print("Starting VeldaOS...")
    veldaos = VeldaOS(openai_api_key=OPENAI_API_KEY)
    print("VeldaOS started")
    with veldaos.open("chrome") as agent:
        agent.loop("Type 'python --version' and read the output")

if __name__ == "__main__":
    asyncio.run(main()) 
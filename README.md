# VeldaOS - AI Agent Marketplace

VeldaOS is a powerful AI agent marketplace and desktop application that enables users to purchase and deploy AI agents that can interact with their operating system through natural user-like actions.

## Features

- AI Agent Marketplace
- Desktop Application for Agent Management
- OS Interaction through Screenshots, Clicks, and Keyboard Input
- Developer SDK for Creating Custom Agents
- Secure Agent Deployment System

## Project Structure

```
veldaos/
├── core/           # Core library for AI agent functionality
├── desktop/        # Desktop application
├── marketplace/    # Agent marketplace system
├── utils/          # OS interaction utilities
└── tests/          # Test suite
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the desktop application:
   ```bash
   python -m veldaos.desktop
   ```

## Development

To create a custom agent:

1. Install the development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
2. Create your agent by extending the base agent class
3. Test your agent using the provided testing framework
4. Package and publish your agent to the marketplace

## License

MIT License - See LICENSE file for details 
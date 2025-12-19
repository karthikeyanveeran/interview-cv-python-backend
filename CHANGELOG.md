# Changelog

All notable changes to the Interview.CV Python Backend will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-19

### Added
- **Complete Agora Conversational AI Integration**
  - Official REST API endpoints (`/api/agora/join`, `/api/agora/agents/{id}/leave`)
  - Webhook handler for all event types (101-110, 201-202)
  - RTC token generation and agent management
  - Customer ID/Secret authentication with base64 encoding

- **Custom LLM Service (OpenAI-Compatible)**
  - Standard chat completions with context awareness
  - RAG-enhanced completions with knowledge retrieval
  - Audio-only output mode with word-level timestamps
  - Multimodal capabilities support

- **Live Transcript Streaming**
  - WebSocket-based real-time transcript delivery
  - Session management and storage
  - Support for user and agent transcripts
  - Status tracking (in_progress, completed, interrupted)

- **Context-Aware Processing**
  - Agora Signaling presence information integration
  - User selections, scores, and interview stages
  - Automatic context enhancement in LLM responses
  - Multi-user presence support

- **Audio Output Mode**
  - Base64-encoded PCM audio streaming
  - Word-level timestamps for subtitle alignment
  - Broadcast mode for direct message playback
  - Context management with transcript storage

- **Core Services**
  - PostgreSQL database with SQLAlchemy ORM
  - Clerk authentication integration
  - Payment processing (Razorpay, Stripe)
  - Cloudflare R2 file storage
  - Redis caching support

### Technical Features
- FastAPI framework with async/await support
- Pydantic models for request/response validation
- WebSocket support for real-time features
- Comprehensive error handling and logging
- Production-ready configuration management

### Testing
- Complete test suite for all major features
- Agora API integration tests
- Custom LLM endpoint validation
- Live transcript functionality tests
- Audio output mode verification
- Context-aware processing tests

### Documentation
- Comprehensive README with setup instructions
- API endpoint documentation
- Configuration guides
- Testing procedures
- Production deployment checklist

## [Unreleased]

### Planned
- Enhanced RAG with vector database integration
- Advanced audio processing capabilities
- Multi-language support
- Performance optimizations
- Additional payment gateway integrations

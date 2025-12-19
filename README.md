# 🎤 Interview.CV Python Backend

Complete Python backend implementation with Agora Conversational AI integration, custom LLM service, live transcripts, and audio output capabilities.

## 🚀 Features

- **🎯 Agora Conversational AI**: Complete REST API integration with official endpoints
- **🤖 Custom LLM Service**: OpenAI-compatible with context awareness and RAG
- **📝 Live Transcripts**: Real-time WebSocket streaming with session management
- **🔊 Audio Output**: Word-level timestamps and broadcast mode support
- **💳 Payment Processing**: Razorpay (India) and Stripe (International)
- **☁️ Cloud Storage**: Cloudflare R2 integration
- **🔐 Authentication**: Clerk integration with secure user management
- **📊 Database**: PostgreSQL with SQLAlchemy ORM

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │  Python Backend  │    │  External APIs  │
│                 │    │                  │    │                 │
│ • Next.js       │◄──►│ • FastAPI        │◄──►│ • Agora         │
│ • React         │    │ • WebSocket      │    │ • OpenAI        │
│ • TypeScript    │    │ • SQLAlchemy     │    │ • Clerk         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📋 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL database
- Agora account with Conversational AI enabled
- OpenAI API key

### Installation

1. **Clone Repository**:
   ```bash
   git clone https://github.com/karthikeyanveeran/interview-cv-python-backend.git
   cd interview-cv-python-backend
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Update with your credentials
   ```

4. **Verify Setup**:
   ```bash
   python verify_setup.py
   ```

5. **Start Server**:
   ```bash
   python run.py
   ```

## 🧪 Testing

Run the complete test suite:
```bash
python test_agora_api.py          # Agora integration tests
python test_custom_llm.py         # Custom LLM endpoints
python test_transcripts.py        # Live transcript features
python test_custom_info.py        # Context processing
python test_audio_output.py       # Audio output mode
```

## 📡 API Endpoints

### Core Services
- `GET /health` - Health check and service status
- `POST /api/users` - User management with Clerk
- `POST /api/upload` - File upload to Cloudflare R2

### Agora Conversational AI
- `POST /api/agora/join` - Start AI agent (official API)
- `POST /api/agora/agents/{id}/leave` - Stop AI agent
- `GET /api/agora/agents/{id}` - Query agent status
- `POST /api/agora/webhook` - Event notifications (101-110, 201-202)

### Custom LLM (OpenAI-Compatible)
- `POST /chat/completions` - Standard completions with context
- `POST /api/rag` - RAG-enhanced with knowledge retrieval
- `POST /api/audio-output` - Audio-only with word timestamps

### Live Transcripts
- `WS /ws/transcripts/{channel}` - Real-time transcript streaming
- `GET /api/transcripts/{channel}` - Session transcript history

### Payments
- `POST /api/payment/razorpay/order` - Razorpay order creation
- `POST /api/payment/stripe/intent` - Stripe payment intent

## 🎯 Key Features

### Agora Integration
```json
{
  "llm": {
    "url": "http://your-backend/api/audio-output",
    "output_modalities": ["audio"],
    "api_key": "internal"
  },
  "advanced_features": {"enable_rtm": true}
}
```

### Audio Output with Timestamps
```json
{
  "choices": [{
    "delta": {
      "audio": {
        "data": "base64_encoded_pcm_data",
        "transcript": "Hello world!",
        "words": [
          {"text": "Hello", "start_ts": 100, "end_ts": 140, "duration": 40}
        ]
      }
    }
  }]
}
```

### Context-Aware Processing
```json
{
  "context": {
    "presence": {
      "candidate": {
        "selection": "Python programming",
        "interview_stage": "technical_round",
        "score": 85
      }
    }
  }
}
```

## 🐳 Docker Deployment

```bash
# Build image
docker build -t interview-cv-backend .

# Run container
docker run -p 8000:8000 --env-file .env interview-cv-backend
```

## 🔧 Configuration

### Required Environment Variables
```env
DATABASE_URL=postgresql://user:pass@host:5432/db
CLERK_SECRET_KEY=sk_test_...
OPENAI_API_KEY=sk-proj-...
NEXT_PUBLIC_AGORA_APP_ID=your_app_id
AGORA_APP_CERTIFICATE=your_certificate
AGORA_CUSTOMER_ID=your_customer_id
AGORA_CUSTOMER_SECRET=your_customer_secret
```

### Optional Services
```env
AZURE_SPEECH_KEY=your_azure_key
REDIS_URL=redis://localhost:6379
R2_ACCESS_KEY_ID=your_r2_key
RAZORPAY_KEY_ID=rzp_test_...
STRIPE_SECRET_KEY=sk_test_...
```

## 📊 Monitoring & Health

- **Health Check**: `GET /health`
- **Metrics**: Built-in FastAPI metrics
- **Logging**: Structured logging with levels
- **Error Tracking**: Comprehensive error handling

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Complete setup guides and API docs
- **Issues**: Report bugs and feature requests on GitHub
- **Setup Help**: Follow `AGORA_SETUP_GUIDE.md` for configuration

---

**Version**: 1.0.0  
**Last Updated**: January 15, 2024  
**Maintainer**: [@karthikeyanveeran](https://github.com/karthikeyanveeran)
# Enterprise RAG - Deployment Guide

## Pre-Deployment Checklist

### Backend
- [ ] FastAPI server configured and tested
- [ ] All endpoints responding correctly
- [ ] CORS enabled for frontend URL
- [ ] Database connections verified
- [ ] Pinecone client initialized
- [ ] Groq LLM API key configured
- [ ] NDJSON streaming working

### Frontend
- [ ] Streamlit dependencies installed
- [ ] CSS loading without errors
- [ ] All pages accessible
- [ ] API client URL configured correctly
- [ ] Session state initialization working
- [ ] Styling matches design

## Local Development

### 1. Environment Setup

```bash
# Navigate to workspace
cd e:\Programs of Diff Languages\Pinecone_RAG

# Create Python virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
pip install -r frontend/requirements.txt
```

### 2. Start Backend

```bash
# From workspace root
python main.py

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000 [Press ENTER to quit]
```

### 3. Start Frontend

In a new terminal:

```bash
# Activate venv if used
venv\Scripts\activate

# From workspace root
streamlit run frontend/app.py

# Expected output:
# Local URL: http://localhost:8501
# Network URL: http://192.168.x.x:8501
```

### 4. Test End-to-End

1. Open http://localhost:8501
2. Select namespace
3. Upload test document (optional)
4. Send test message
5. Verify:
   - Message appears
   - Tokens stream in real-time
   - Sources show after complete
   - Session is saved

## Production Deployment

### Option 1: Docker Deployment

#### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt frontend/requirements.txt ./
RUN pip install -r requirements.txt && \
    pip install -r frontend/requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose ports
EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start both services
CMD ["sh", "-c", "python main.py & streamlit run frontend/app.py"]
```

#### Build & Run

```bash
# Build image
docker build -t enterprise-rag:latest .

# Run container
docker run -p 8000:8000 -p 8501:8501 \
  -e GROQ_API_KEY=your_key \
  -e PINECONE_API_KEY=your_key \
  enterprise-rag:latest
```

### Option 2: Cloud Deployment (Streamlit Cloud)

1. Push repo to GitHub
2. Go to https://streamlit.io/cloud
3. Deploy: "New app" → Select repo
4. Set secrets in Settings:
   ```
   GROQ_API_KEY = your_key
   PINECONE_API_KEY = your_key
   BASE_URL = your_backend_url
   ```

**Note:** Backend still needs separate hosting (Heroku, AWS, GCP, etc.)

### Option 3: Linux Server Deployment

#### Setup

```bash
# SSH to server
ssh user@server_ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# Clone repository
git clone https://github.com/yourusername/enterprise-rag.git
cd enterprise-rag

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r frontend/requirements.txt
```

#### Configure systemd Services

**Backend service** (`/etc/systemd/system/rag-backend.service`):

```ini
[Unit]
Description=Enterprise RAG Backend
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/home/appuser/enterprise-rag
Environment="PATH=/home/appuser/enterprise-rag/venv/bin"
Environment="GROQ_API_KEY=your_key"
Environment="PINECONE_API_KEY=your_key"
ExecStart=/home/appuser/enterprise-rag/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Frontend service** (`/etc/systemd/system/rag-frontend.service`):

```ini
[Unit]
Description=Enterprise RAG Frontend
After=network.target rag-backend.service

[Service]
Type=simple
User=appuser
WorkingDirectory=/home/appuser/enterprise-rag
Environment="PATH=/home/appuser/enterprise-rag/venv/bin"
ExecStart=/home/appuser/enterprise-rag/venv/bin/streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Enable Services

```bash
sudo systemctl daemon-reload
sudo systemctl enable rag-backend rag-frontend
sudo systemctl start rag-backend rag-frontend

# Check status
sudo systemctl status rag-backend
sudo systemctl status rag-frontend

# View logs
sudo journalctl -u rag-backend -f
sudo journalctl -u rag-frontend -f
```

#### Configure Nginx Reverse Proxy

```nginx
upstream backend {
    server 127.0.0.1:8000;
}

upstream frontend {
    server 127.0.0.1:8501;
}

server {
    listen 80;
    server_name your.domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your.domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Backend API
    location /api/ {
        proxy_pass http://backend/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_buffering off;
    }

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

### Option 4: AWS Deployment

#### Using EC2 + ECS

1. **Create EC2 instance**
   - Ubuntu 22.04 LTS
   - t3.medium (2GB RAM minimum)
   - Security group: Allow 80, 443, 8000, 8501

2. **Build Docker image**
   ```bash
   docker build -t enterprise-rag:latest .
   docker tag enterprise-rag:latest your_account.dkr.ecr.us-east-1.amazonaws.com/enterprise-rag:latest
   docker push your_account.dkr.ecr.us-east-1.amazonaws.com/enterprise-rag:latest
   ```

3. **Create ECS task definition**
   ```json
   {
     "family": "enterprise-rag",
     "containerDefinitions": [
       {
         "name": "rag",
         "image": "your_account.dkr.ecr.us-east-1.amazonaws.com/enterprise-rag:latest",
         "portMappings": [
           {"containerPort": 8000},
           {"containerPort": 8501}
         ],
         "environment": [
           {"name": "GROQ_API_KEY", "value": "your_key"},
           {"name": "PINECONE_API_KEY", "value": "your_key"}
         ]
       }
     ]
   }
   ```

4. **Create ECS service** with ALB

## Environment Variables

### Required
```
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_index
```

### Optional
```
BACKEND_URL=http://backend:8000
FRONTEND_PORT=8501
LOG_LEVEL=info
```

## Monitoring & Maintenance

### Log Monitoring
```bash
# Backend logs
tail -f /var/log/rag-backend.log

# Frontend logs
tail -f /var/log/rag-frontend.log
```

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Frontend accessibility
curl http://localhost:8501
```

### Performance Optimization

1. **Enable caching**
   - Redis for session cache
   - CDN for static assets

2. **Database optimization**
   - Regular Pinecone index maintenance
   - Monitor token usage

3. **Rate limiting**
   - Implement on backend API
   - Prevent DDoS attacks

4. **Load balancing**
   - Multiple backend instances
   - Sticky sessions for state

## Backup & Recovery

```bash
# Backup sessions and documents
tar -czf backup-$(date +%Y%m%d).tar.gz \
  app/core/ \
  app/services/ \
  uploaded_docs/

# Backup to S3
aws s3 cp backup-*.tar.gz s3://your-bucket/backups/

# Restore from backup
tar -xzf backup-20231215.tar.gz
```

## Troubleshooting

### Backend not responding
```bash
# Check if running
ps aux | grep "python main.py"

# Check logs
tail -f logs/backend.log

# Restart
systemctl restart rag-backend
```

### Frontend connection errors
```bash
# Verify backend URL in api_client.py
grep BASE_URL frontend/services/api_client.py

# Test connectivity
curl -v http://localhost:8000/namespaces
```

### High memory usage
```bash
# Check process memory
ps aux | grep streamlit

# Monitor system
watch -n 1 'free -h && echo --- && ps aux | grep rag'

# Optimize: Reduce cache size in config
```

## Rollback Procedure

```bash
# Stop services
systemctl stop rag-backend rag-frontend

# Revert to previous version
git checkout previous_commit_hash

# Reinstall dependencies
pip install -r requirements.txt

# Start services
systemctl start rag-backend rag-frontend
```

---

**Version**: 1.0  
**Last Updated**: 2024  
**Status**: Production Ready ✅

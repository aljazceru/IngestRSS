# 🚀 IngestRSS -

### Prerequisites

- Python 3.12
- Docker installed and running

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/IngestRSS.git
   cd IngestRSS
   ```

2. Install required packages:
   ```
   python -m pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Copy `local.env.template` to `.env` in the project root.
   - Open the `.env` file and fill in the values marked with `***` (MinIO credentials, bucket name, etc.).

4. Launch the application:
   ```
   docker compose up --build
   ```
   This will start MongoDB, Redis, MinIO and the worker/scheduler services. You can also run `python launch.py --local` which performs the same action.

## 🛠️ Configuration

- **RSS feeds can be modified in the `rss_feeds.json` file.**
- Environment variables are loaded from the `.env` file created from `local.env.template`.
- Docker services are defined in `docker-compose.yml`.
- Lambda function code (used by the local worker) lives in `src/infra/lambdas/RSSFeedProcessorLambda/src/`.



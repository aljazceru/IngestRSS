# 🚀 IngestRSS - 🗞️💵⚖️

![Header](wallpaper.png)

IngestRSS is a Docker-based RSS feed processing system that automatically fetches, processes, and stores articles from specified RSS feeds. This project is designed to support social scientists in progressing research on news and media. The application can now run entirely on your local machine without any AWS dependencies.

## 🎯 Purpose

The primary goal of IngestRSS is to provide researchers with a robust, scalable solution for collecting and analyzing large volumes of news data. By automating the process of gathering articles from diverse sources, this tool enables social scientists to focus on their research questions and data analysis, rather than the complexities of data collection.

## 🚀 Getting Started

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

## 📊 Monitoring

Logs from the worker and scheduler are printed to the console. Metrics are
exposed using [Prometheus](https://prometheus.io/). When the processor runs it
starts a tiny HTTP server that serves metrics on `/metrics` (port `8000` by
default). These metrics can be scraped by a Prometheus server for monitoring.

## 🤝 Contributing

Contributions are welcome, feel free to see open issues to get started. 


## 📄 License

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


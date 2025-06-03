"""Prometheus metrics utilities for the RSS feed processor."""

import os
from prometheus_client import Counter, Histogram, start_http_server


# Start a Prometheus metrics HTTP server exposing ``/metrics``. The port can be
# customised with the ``METRICS_PORT`` environment variable. This block is safe
# to run multiple times as it silently ignores port binding errors.
_metrics_port = int(os.environ.get("METRICS_PORT", "8000"))
if not os.environ.get("METRICS_SERVER_STARTED"):
    try:
        start_http_server(_metrics_port)
        os.environ["METRICS_SERVER_STARTED"] = "1"
    except OSError:
        pass


# Metric definitions
_processed_articles = Counter(
    "processed_articles_total",
    "Total number of processed articles",
)
_processing_time = Histogram(
    "rss_processing_seconds",
    "Time spent processing RSS feeds",
)
_extraction_errors = Counter(
    "extraction_errors_total",
    "Number of article extraction errors",
)


def record_processed_articles(count: int) -> None:
    """Increment the processed articles counter."""
    _processed_articles.inc(count)


def record_processing_time(duration: float) -> None:
    """Record how long a feed took to process."""
    _processing_time.observe(duration)


def record_extraction_errors(count: int) -> None:
    """Increment the extraction errors counter."""
    _extraction_errors.inc(count)

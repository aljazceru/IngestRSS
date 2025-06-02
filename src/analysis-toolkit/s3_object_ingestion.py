from minio import Minio
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict

def get_s3_object_creation_dates(bucket_name):
    client = Minio(
        os.getenv("MINIO_ENDPOINT"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False
    )
    creation_dates = []

    for obj in client.list_objects(bucket_name, recursive=True):
        creation_dates.append(obj.last_modified.date())

    return creation_dates

def plot_creation_dates(dates):
    # Count objects created on each date
    date_counts = defaultdict(int)
    for date in dates:
        date_counts[date] += 1

    # Sort dates and get counts
    sorted_dates = sorted(date_counts.keys())
    counts = [date_counts[date] for date in sorted_dates]

    # Create the plot
    plt.figure(figsize=(15, 8))
    bars = plt.bar(sorted_dates, counts)
    plt.title('S3 Object Creation Dates')
    plt.xlabel('Date')
    plt.ylabel('Number of Objects Created')
    plt.xticks(rotation=45, ha='right')

    # Label each bar with its height
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}',
                 ha='center', va='bottom')

    plt.tight_layout()

    # Save the plot
    plt.savefig('s3_object_creation_dates.png', dpi=300, bbox_inches='tight')
    print("Graph saved as 's3_object_creation_dates.png'")

def main():
    bucket_name = os.getenv('MINIO_BUCKET')
    dates = get_s3_object_creation_dates(bucket_name)
    plot_creation_dates(dates)

if __name__ == "__main__":
    main()
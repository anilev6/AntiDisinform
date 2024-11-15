from google.cloud import bigquery
import os


def initialize_bigquery_client():
    """
    Initialize a BigQuery client explicitly using the service account JSON file path
    from an environment variable.

    Returns:
        google.cloud.bigquery.Client: BigQuery client instance.
    """
    # Get the path to the service account JSON file from an environment variable
    service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    if not service_account_path:
        raise EnvironmentError(
            "The environment variable 'GOOGLE_APPLICATION_CREDENTIALS' is not set."
        )

    # Initialize the BigQuery client explicitly with the service account JSON
    client = bigquery.Client.from_service_account_json(service_account_path)

    return client


# Example usage
if __name__ == "__main__":
    # Initialize the BigQuery client
    bigquery_client = initialize_bigquery_client()

    # Example operation: List datasets in the project
    res = [x for x in bigquery_client.query("SELECT * FROM `atreus.main` LIMIT 5").result()]
    print(res)

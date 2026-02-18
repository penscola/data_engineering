"""Template for building a `dlt` pipeline to ingest data from a REST API."""

import dlt
from dlt.sources.rest_api import rest_api_resources


# if no argument is provided, `access_token` is read from `.dlt/secrets.toml`
@dlt.source
def open_library_source(query: str = "harry potter"):

    return rest_api_resources({
        "client": {
            "base_url": "https://openlibrary.org",
        },
        "resource_defaults": {
            "primary_key": "key",
            "write_disposition": "replace",
        },
        "resources": [
            {
                "name": "books",
                "endpoint": {
                    "path": "search.json",
                    "params": {
                        "q": query,
                        "limit": 100,
                    },
                    "data_selector": "docs",
                    "paginator": {
                        "type": "offset",
                        "limit": 100,
                        "offset_param": "offset",
                        "limit_param": "limit",
                        "total_path": "numFound",
                    },
                },
            },
        ],
    })


pipeline = dlt.pipeline(
    pipeline_name="open_library_pipeline",
    destination="duckdb",
    dataset_name="ol_data",
    progress="log"  # logs the pipeline run (Optional)
)


if __name__ == "__main__":
    load_info = pipeline.run(open_library_source())
    print(load_info)  # noqa: T201

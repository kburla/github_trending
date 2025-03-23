# Trending GitHub Repositories Data Pipeline

A simple ETL (Extract, Transform, Load) pipeline that scrapes trending GitHub repositories, processes the data, stores it in a database, and visualizes it in a Streamlit app.

## Components

### DAGs

- **github_trending.py**: Defines the Airflow DAG for the GitHub trending pipeline. It schedules tasks to scrape GitHub trending data and insert it into the database.

### Source Files

- **scraper.py**: Contains functions to scrape GitHub trending repositories and create database tables.
- **insert_data.py**: Contains functions to insert scraped data into the database.
- **database.py**: Sets up the database connection and defines functions to create and drop tables.
- **models.py**: Defines the database models for daily, weekly, and monthly trending repositories.
- **viz.py**: Streamlit app to visualize the trending GitHub repositories data.

## Setup

### Prerequisites

- Python 3.12
- Apache Airflow
- SQLite

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/github_trending_pipeline.git
    cd github_trending_pipeline
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Initialize Airflow**:
    ```sh
    airflow db init
    ```

5. **Create a symlink for the DAG**:
    ```sh
    ln -s /<project directory>/github_trending_pipeline/dags/github_trending.py ~/airflow/dags/github_trending.py
    ```

### Configuration

1. **Start the Airflow web server**:
    ```sh
    airflow webserver --port 8080
    ```

2. **Start the Airflow scheduler**:
    In a new terminal window, start the Airflow scheduler:
    ```sh
    airflow scheduler
    ```

3. **Access the Airflow UI**:
    Open your web browser and go to `http://localhost:8080`. You should see the Airflow UI.

4. **Enable and trigger the DAG**:
    - In the Airflow UI, you should see your `github_trending_pipeline` DAG listed.
    - Toggle the DAG to "On" to enable it.
    - Click on the DAG name to go to the DAG details page.
    - Click the "Trigger DAG" button to manually trigger the DAG.

### Running the Streamlit App

1. **Start the Streamlit app**:
    ```sh
    streamlit run src/viz.py
    ```

2. **Access the Streamlit app**:
    Open your web browser and go to `http://localhost:8501`. You should see the Streamlit app displaying the trending GitHub repositories data.

## Usage

The pipeline scrapes GitHub trending repositories and stores the data in a SQLite database. The data is categorized into daily, weekly, and monthly trending repositories.

### Viewing Logs

To view the logs of a task instance:
1. In the Airflow UI, navigate to the DAG details page.
2. Click on the task instance name to view the details.
3. Click on the "Log" button to view the logs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Apache Airflow](https://airflow.apache.org/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Streamlit](https://streamlit.io/)
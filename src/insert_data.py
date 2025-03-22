from database import Session
from models import DailyTrendingRepo, WeeklyTrendingRepo, MonthlyTrendingRepo
from datetime import datetime, timedelta

def insert_data(repos_data, trending_type):
    session = Session()
    now = datetime.now()
    rows_inserted = 0
    rows_updated = 0
    
    # set interval
    half_hour_ago = now - timedelta(hours=0.5)
    
    match trending_type:
        case 'daily':
            RepoModel = DailyTrendingRepo
            trending_value = now.date()
        case 'weekly':
            RepoModel = WeeklyTrendingRepo
            trending_value = now.isocalendar()[1]
        case 'monthly':
            RepoModel = MonthlyTrendingRepo
            trending_value = now.month
        case _:
            raise ValueError("Invalid trending type. Must be 'daily', 'weekly', or 'monthly'.")

    for repo in repos_data:
        # check for rows with datetime of up to an hour ago
        existing_repo = session.query(RepoModel).filter(RepoModel.url == repo["url"], RepoModel.date >= half_hour_ago).first()
        if existing_repo is None:
            new_repo = RepoModel(
                name = repo["name"],
                description = repo["description"],
                language = repo["language"],
                stars = repo["stars"],
                forks = repo["forks"],
                url = repo["url"],
                date = now
            )
            if trending_type == 'daily':
                new_repo.trending_date = trending_value
            elif trending_type == 'weekly':
                new_repo.trending_week = trending_value
            elif trending_type == 'monthly':
                new_repo.trending_month = trending_value
            session.add(new_repo)
            rows_inserted += 1
    session.commit()
    session.close()
    print(f"{rows_inserted} new rows inserted and {rows_updated} rows updated successfully into {trending_type} trending repos!")

# Example usage
if __name__ == "__main__":
    example_data = [
        {
            "name": "example_repo",
            "description": "An example repository",
            "language": "Python",
            "stars": 1000,
            "forks": 100,
            "url": "https://github.com/example/example_repo"
        }
    ]
    insert_data(example_data, 'daily')
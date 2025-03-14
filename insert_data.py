from database import Session
from models import DailyTrendingRepo, WeeklyTrendingRepo, MonthlyTrendingRepo
from datetime import date

def insert_data(repos_data, trending_type):
    session = Session()
    today = date.today()
    rows_inserted = 0
    
    match trending_type:
        case 'daily':
            RepoModel = DailyTrendingRepo
        case 'weekly':
            RepoModel = WeeklyTrendingRepo
        case 'monthly':
            RepoModel = MonthlyTrendingRepo
        case _:
            raise ValueError("Invalid trending type. Must be 'daily', 'weekly', or 'monthly'.")

    for repo in repos_data:
        existing_repo = session.query(RepoModel).filter_by(name=repo["name"], date=today).first()
        if existing_repo is None:
            new_repo = RepoModel(
                name = repo["name"],
                description = repo["description"],
                language = repo["language"],
                stars = int(repo["stars"].replace(",", "")),  # Convert to int
                forks = int(repo["forks"].replace(",", "")),  # Convert to int
                url = repo["url"],
                date = today
            )
            session.add(new_repo)
            rows_inserted += 1
    session.commit()
    session.close()
    print(f"✅ {rows_inserted} new rows inserted successfully into {trending_type} trending repos!")

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
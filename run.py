from app import create_app, scheduler
from app.routes import sbert

app = create_app()

if __name__ == "__main__":
    app.run()

    scheduler.add_job(id='Update Task', func=sbert.update_all_embeddings(), trigger='interval', hours=24)

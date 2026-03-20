from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.review import Review

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/")
def create_review(
    city_id: int,
    user_name: str,
    money_spent: float,
    trip_days: int,
    value_rating: float,
    comment: str
):
    db = SessionLocal()

    # simple validation for rating  must be between 0 and 5 
    if value_rating < 0 or value_rating > 5:
        db.close()
        raise HTTPException(status_code=400, detail="Rating must be between 0 and 5")

# create review object
    review = Review(
        city_id=city_id,
        user_name=user_name,
        money_spent=money_spent,
        trip_days=trip_days,
        value_rating=value_rating,
        comment=comment
    )

    db.add(review)
    db.commit()
    db.refresh(review)
    db.close()

    return review

@router.get("/city/{city_id}")
def get_reviews_by_city(city_id: int):
    db = SessionLocal()

    reviews = db.query(Review).filter(
        Review.city_id == city_id
    ).all()

    db.close()


# if no reviews found → return message
    if not reviews:
        return {
            "city_id": city_id,
            "message": "No reviews found for this city",
            "reviews": []
        }

    return {
        "city_id": city_id,
        "total_reviews": len(reviews),
        "reviews": reviews
    }
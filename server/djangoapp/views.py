# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
# ...

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...

# Task 9: Return all dealerships for the frontend/API request
def get_dealerships(request):
    import json
    from pathlib import Path
    from django.http import JsonResponse

    data_file = Path(__file__).resolve().parents[1] / "database" / "data" / "dealerships.json"

    try:
        with open(data_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        return JsonResponse({
            "status": 200,
            "dealers": data["dealerships"]
        })
    except (OSError, ValueError, KeyError) as error:
        return JsonResponse({
            "status": 500,
            "error": str(error)
        }, status=500)

# Task 10: Return one dealership by ID
def get_dealer_by_id(request, dealer_id):
    import json
    from pathlib import Path
    from django.http import JsonResponse

    data_file = Path(__file__).resolve().parents[1] / "database" / "data" / "dealerships.json"

    try:
        with open(data_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        dealer = next(
            (item for item in data["dealerships"] if str(item["id"]) == str(dealer_id)),
            None
        )

        if dealer is None:
            return JsonResponse({"error": "Dealer not found"}, status=404)

        return JsonResponse({"status": 200, "dealer": dealer})

    except (OSError, ValueError, KeyError) as error:
        return JsonResponse({"error": str(error)}, status=500)

# Task 11: Return dealerships located in a specified state
def get_dealers_by_state(request, state):
    import json
    from pathlib import Path
    from django.http import JsonResponse

    data_file = Path(__file__).resolve().parents[1] / "database" / "data" / "dealerships.json"

    try:
        with open(data_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        dealers = [
            dealer for dealer in data["dealerships"]
            if dealer["state"].lower() == state.lower()
        ]

        return JsonResponse({"status": 200, "dealers": dealers})

    except (OSError, ValueError, KeyError) as error:
        return JsonResponse({"error": str(error)}, status=500)

# Task 14: Get all car makes and models
def get_car_make(request):
    import json
    from pathlib import Path
    from django.http import JsonResponse

    data_file = Path(__file__).resolve().parents[1] / "database" / "data" / "car_records.json"

    try:
        with open(data_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        cars = [
            {"make": car["make"], "model": car["model"]}
            for car in data["cars"]
        ]

        return JsonResponse({"status": 200, "CarMakes": cars})

    except (OSError, ValueError, KeyError) as error:
        return JsonResponse({"error": str(error)}, status=500)

def get_dealer_reviews(request, dealer_id):
    from pathlib import Path

    data_file = (
        Path(__file__).resolve().parents[1]
        / "database" / "data" / "reviews.json"
    )

    try:
        with open(data_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        reviews = [
            review for review in data["reviews"]
            if str(review["dealership"]) == str(dealer_id)
        ]

        return JsonResponse({
            "status": 200,
            "reviews": reviews
        })

    except (OSError, ValueError, KeyError) as error:
        return JsonResponse({
            "status": 500,
            "error": str(error)
        }, status=500)


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse(
            {"status": 405, "error": "POST method required"},
            status=405
        )

    try:
        from pathlib import Path

        data_file = (
            Path(__file__).resolve().parents[1]
            / "database" / "data" / "reviews.json"
        )

        with open(data_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        review_data = json.loads(request.body.decode("utf-8"))

        required_fields = [
            "name", "dealership", "review", "purchase",
            "purchase_date", "car_make", "car_model", "car_year"
        ]

        if any(
            field not in review_data or str(review_data[field]).strip() == ""
            for field in required_fields
        ):
            return JsonResponse(
                {"status": 400, "error": "All review fields are required"},
                status=400
            )

        review_data["id"] = max(
            (int(item.get("id", 0)) for item in data.get("reviews", [])),
            default=0
        ) + 1

        review_data["dealership"] = int(review_data["dealership"])
        review_data["car_year"] = int(review_data["car_year"])

        data.setdefault("reviews", []).append(review_data)

        with open(data_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        return JsonResponse({
            "status": 200,
            "message": "Review added successfully"
        })

    except (ValueError, TypeError, OSError, KeyError) as error:
        return JsonResponse(
            {"status": 400, "error": str(error)},
            status=400
        )


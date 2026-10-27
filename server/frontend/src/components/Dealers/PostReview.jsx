
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const { id } = useParams();

  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  const dealer_url = `/djangoapp/get_dealer/${id}`;
  const review_url = `/djangoapp/add_review`;
  const carmodels_url = `/djangoapp/get_car_make`;

  useEffect(() => {
    const getDealer = async () => {
      try {
        const res = await fetch(dealer_url);
        const data = await res.json();

        if (res.ok && data.status === 200) {
          setDealer(data.dealer);
        }
      } catch (error) {
        console.error("Error loading dealer:", error);
      }
    };

    const getCars = async () => {
      try {
        const res = await fetch(carmodels_url);
        const data = await res.json();

        console.log("Car make API response:", data);

        if (res.ok && data.status === 200) {
          setCarmodels(data.CarModels || data.CarMakes || []);
        }
      } catch (error) {
        console.error("Error loading car makes:", error);
      }
    };

    getDealer();
    getCars();
  }, [id]);

  const postreview = async () => {
    if (!model || !review.trim() || !date || !year) {
      alert("All details are mandatory");
      return;
    }

    const selectedCar = carmodels.find(
      (car) => `${car.CarMake} ${car.CarModel}` === model
    );

    const parts = model.split(" ");
    const makeChosen = selectedCar?.CarMake || parts[0];
    const modelChosen = selectedCar?.CarModel || parts.slice(1).join(" ");

    let name =
      `${sessionStorage.getItem("firstname")} ${sessionStorage.getItem("lastname")}`;

    if (name.includes("null")) {
      name = sessionStorage.getItem("username") || "User";
    }

    const jsoninput = {
      name,
      dealership: id,
      review: review.trim(),
      purchase: true,
      purchase_date: date,
      car_make: makeChosen,
      car_model: modelChosen,
      car_year: year
    };

    try {
      const res = await fetch(review_url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(jsoninput)
      });

      const data = await res.json();

      if (res.ok && data.status === 200) {
        window.location.href = `/dealer/${id}`;
      } else {
        alert(data.error || "Could not submit review. Please check the server.");
      }
    } catch (error) {
      console.error("Error submitting review:", error);
      alert("Could not submit review. Check that the Django server is running.");
    }
  };

  return (
    <div>
      <Header />

      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name}</h1>

        <textarea
          id="review"
          cols="50"
          rows="7"
          value={review}
          onChange={(e) => setReview(e.target.value)}
          placeholder="Write your review"
        />

        <div className="input_field">
          Purchase Date{" "}
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div className="input_field">
          Car Make
          <select
            name="cars"
            id="cars"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="" disabled>
              Choose Car Make and Model
            </option>

            {carmodels.map((car, index) => {
              const make = car.CarMake || car.make || car.name;
              const carModel = car.CarModel || car.model || "";

              if (!make) return null;

              const value = `${make} ${carModel}`.trim();

              return (
                <option key={car.id || index} value={value}>
                  {value}
                </option>
              );
            })}
          </select>

          {carmodels.length === 0 && (
            <p>Car makes are loading or unavailable. Please check the API.</p>
          )}
        </div>

        <div className="input_field">
          Car Year{" "}
          <input
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            max="2023"
            min="2015"
          />
        </div>

        <div>
          <button className="postreview" onClick={postreview}>
            Post Review
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;

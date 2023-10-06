import React, { useState, useEffect } from "react";
import axios from "axios";
import Fightcard from "./Fightcard";
import Select from "react-select";
// import fighters from "./fighter_names.json";

function Dashboard() {
  const fetchFighterData = (e) => {
    e.preventDefault();
    let fighterObject = {
      fighter1: fighterName1,
      fighter2: fighterName2,
    };
    axios
      .post(`/predict`, fighterObject)
      .then((response) => {
        let fighter1 = { fighter: response.data.fighter1 };
        let fighter2 = { fighter: response.data.fighter2 };
        let prediction = response.data.prediction;
        setFighter1Data(fighter1);
        setFighter2Data(fighter2);
        setPrediction(prediction);
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
        if (error.response) {
          let errorMessage = error.response.data;
          alert(errorMessage);
        }
      });
  };

  const [fighterName1, setFighterName1] = useState("");
  const [fighterName2, setFighterName2] = useState("");

  const [fighter1Data, setFighter1Data] = useState({
    fighter: {
      draws: 0,
      height: "",
      image_url: false,
      losses: 0,
      name: "",
      nickname: "",
      reach: "",
      stance: "",
      weight: "",
      wins: 0,
    },
  });
  const [fighter2Data, setFighter2Data] = useState({
    fighter: {
      draws: 0,
      height: "",
      image_url: false,
      losses: 0,
      name: "",
      nickname: "",
      reach: "",
      stance: "",
      weight: "",
      wins: 0,
    },
  });

  const [prediction, setPrediction] = useState("");

  const [fighters, setFighters] = useState([]);

  useEffect(() => {
    fetch("/fighter_names.json")
      .then((response) => response.json())
      .then((data) => setFighters(data));
  }, []);

  // Mock data for a fighter
  const mockFighterData = {
    fighter: {
      name: "Jon Jones",
      nickname: "Bones",
      height: "6'4\"",
      reach: "84 inches",
      weight: "205 lbs",
      wins: 26,
      losses: 1,
      draws: 0,
      stance: "Orthodox",
      image_url:
        "https://dmxg5wxfqgb4u.cloudfront.net/styles/athlete_bio_full_body/s3/2023-03/JONES_JON_L_BELT_03_04.png?itok=P6J6DQpm",
    },
  };

  const selectStyles = {
    control: (base) => ({
      ...base,
      color: "#000",
    }),
    singleValue: (base) => ({
      ...base,
      color: "#000",
    }),
    option: (base) => ({
      ...base,
      color: "#000",
    }),
  };

  return (
    <div className="container">
      <div className="fighter-card">
        {/* <Fightcard fighter_data={mockFighterData} /> */}
        {fighter1Data.fighter && <Fightcard fighter_data={fighter1Data} />}
        <div className="analysis"></div>
      </div>
      <div className="predictor-column">
        <div className="predictor-title">
          <h1>FIGHT PREDICTOR</h1>
        </div>
        <div className="predictor-form">
          <div>
            <form onSubmit={fetchFighterData}>
              <label>
                Fighter 1:
                <Select
                  options={fighters}
                  value={{ value: fighterName1, label: fighterName1 }}
                  onChange={(selectedOption) =>
                    setFighterName1(selectedOption.value)
                  }
                  styles={selectStyles}
                />
              </label>
              <label>
                Fighter 2:
                <Select
                  options={fighters}
                  value={{ value: fighterName2, label: fighterName2 }}
                  onChange={(selectedOption) =>
                    setFighterName2(selectedOption.value)
                  }
                  styles={selectStyles}
                />
              </label>
              <button type="submit">Predict</button>
            </form>
          </div>
          <div className="predictor-prediction">
            <p>{prediction}</p>
          </div>
        </div>
      </div>
      <div className="fighter-card">
        {/* <Fightcard fighter_data={mockFighterData} /> */}
        {fighter1Data.fighter && <Fightcard fighter_data={fighter2Data} />}
      </div>
    </div>
  );
}

export default Dashboard;

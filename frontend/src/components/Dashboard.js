import React, { useState, useEffect } from "react";
import axios from "axios";
import Fightcard from "./Fightcard";


const host = "http://0.0.0.0:5001:8000";

function Dashboard() {
  const fetchFighterData = (e) => {
    e.preventDefault();
    let fighterObject = {
      fighter1: fighterName1,
      fighter2: fighterName2,
    };
    axios
      .post(`${host}/predict`, fighterObject)
      .then((response) => {
        let fighter1 = { fighter: response.data.fighter1};
        let fighter2 = { fighter: response.data.fighter2};
        let prediction = response.data.prediction;
        setFighter1Data(fighter1);
        setFighter2Data(fighter2);
        setPrediction(prediction);
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
        if(error.response){
          let errorMessage = error.response.data;
          alert(errorMessage)
        }
      });
  };

  const [fighterName1, setFighterName1] = useState("");
  const [fighterName2, setFighterName2] = useState("");

  const [fighter1Data, setFighter1Data] = useState({
    fighter: {
      draws: 0,
      height: '',
      image_url: false,
      losses: 0,
      name: "",
      nickname: "",
      reach: '',
      stance: "",
      weight: "",
      wins: 0,
    },
  });
  const [fighter2Data, setFighter2Data] = useState({
    fighter: {
      draws: 0,
      height: '',
      image_url: false,
      losses: 0,
      name: "",
      nickname: "",
      reach: '',
      stance: "",
      weight: "",
      wins: 0,
    },
  });

  const [prediction, setPrediction] = useState("");

  useEffect(() => {
    // Fetch data here
  }, []);

  return (
    <div className="container">
      <div className="column">
        {fighter1Data.fighter && <Fightcard fighter_data={fighter1Data} />}
        <div className="analysis">
        </div>
      </div>
      <div className="column">
        <div className="predictor">
          <div>
            <h1>FIGHT PREDICTOR</h1>
          </div>
          <div>
            <form onSubmit={fetchFighterData}>
              <label>
                Fighter 1:
                <input
                  type="text"
                  value={fighterName1}
                  onChange={(e) => setFighterName1(e.target.value)}  
                />
              </label>
              <label>
                Fighter 2:
                <input
                  type="text"
                  value={fighterName2}
                  onChange={(e) => setFighterName2(e.target.value)}  
                />
              </label>
              <button type="submit">Predict</button>
            </form>
          </div>
          <div>
            <p>{prediction}</p>
          </div>
        </div>
      </div>
      <div className="column">
      {fighter1Data.fighter && <Fightcard fighter_data={fighter2Data} />}
      </div>
    </div>
  );
}

export default Dashboard;

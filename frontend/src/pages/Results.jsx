import { useEffect, useState } from "react";
import "../Styles/Results.css";

function Results(){

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);


  useEffect(()=>{

    fetch("http://127.0.0.1:5000/api/results")

    .then(response => response.json())

    .then(data => {

      setResult(data);
      setLoading(false);

    })

    .catch(error => {

      console.log("Error:", error);
      setLoading(false);

    });

  },[]);



  return(

    <div className="results-page">


      <h1>Decision Results</h1>


      {
        loading && (

          <h2>
            Generating Results...
          </h2>

        )
      }



      {
        result && (

          <div className="result-card">


            <h2>
              {result.scenario}
            </h2>


            <p>
              <b>Prediction:</b> {result.prediction}
            </p>


            <p>
              <b>Customer Impact:</b> {result.customer_impact}
            </p>


            <p>
              <b>Revenue Impact:</b> {result.revenue_impact}
            </p>


            <h3>
              Confidence: {result.confidence}
            </h3>


            <p>
              <b>Recommendation:</b> {result.recommendation}
            </p>


          </div>

        )
      }


    </div>

  );

}


export default Results;
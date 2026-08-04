import { useEffect, useState } from "react";
import "../Styles/Simulation.css";

function Simulation(){

    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(true);


    useEffect(()=>{

        fetch("http://127.0.0.1:5000/api/simulation")

        .then(response => response.json())

        .then(data => {

            setResult(data);
            setLoading(false);

        })

        .catch(error=>{

            console.log("Error:", error);
            setLoading(false);

        });

    },[]);



    return(

        <div className="simulation-page">


            <h1>AI Simulation</h1>


            {
                loading && (

                    <h2>
                        Running Simulation...
                    </h2>

                )
            }



            {
                result && (

                    <div className="simulation-card">


                        <h2>
                            {result.scenario}
                        </h2>


                        <p>
                            <b>Impact:</b> {result.impact}
                        </p>


                        <p>
                            <b>Customer Change:</b> {result.customer_change}
                        </p>


                        <p>
                            <b>Revenue Change:</b> {result.revenue_change}
                        </p>


                        <h3>
                            Confidence: {result.confidence}
                        </h3>


                    </div>

                )
            }


        </div>

    );

}


export default Simulation;
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


            <h1>AI Simulation Engine</h1>


            {
                loading && (

                    <h2>
                        🤖 Running Simulation...
                    </h2>

                )
            }



            {
                result && (

                    <div className="simulation-card">


                        <h2>
                            Simulation Results
                        </h2>


                        <p>
                            <b>Total Synthetic Users Tested:</b>
                            {" "}
                            {result.total_users}
                        </p>


                        <p>
                            <b>Users Adopted:</b>
                            {" "}
                            {result.adopted_users}
                        </p>


                        <p>
                            <b>Users Rejected:</b>
                            {" "}
                            {result.rejected_users}
                        </p>


                        <h3>
                            Adoption Rate:
                            {" "}
                            {result.adoption_rate}
                        </h3>


                        <h3>
                            Prediction:
                            {" "}
                            {result.prediction}
                        </h3>


                    </div>

                )
            }


        </div>

    );

}


export default Simulation;
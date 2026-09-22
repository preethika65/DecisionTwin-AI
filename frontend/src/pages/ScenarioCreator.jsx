import { useState } from "react";
import "../Styles/ScenarioCreator.css";

function ScenarioCreator() {

  const [formData, setFormData] = useState({
    product: "",
    audience: "",
    research: "",
    count: ""
  });

  const [loading, setLoading] = useState(false);


  const handleChange = (e) => {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });

  };


  const generatePersonas = async () => {

    setLoading(true);


    try {

      const response = await fetch(
        "http://127.0.0.1:5000/api/generate-personas",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify(formData)
        }
      );


      const data = await response.json();


      if(response.ok){

        alert(
          `${data.message} (${data.count} personas created)`
        );


        setFormData({
          product:"",
          audience:"",
          research:"",
          count:""
        });

      }
      else{

        alert(data.error);

      }


    }

    catch(error){

      console.log(error);

      alert("Generation failed");

    }


    finally{

      setLoading(false);

    }

  };



  return (

    <div className="scenario-page">


      <h1>
        Synthetic Persona Generator
      </h1>


      <p>
        Generate synthetic users for AI simulations.
      </p>



      <input
        name="product"
        placeholder="Product description"
        value={formData.product}
        onChange={handleChange}
      />



      <input
        name="audience"
        placeholder="Target audience"
        value={formData.audience}
        onChange={handleChange}
      />



      <input
        name="research"
        placeholder="Research objective"
        value={formData.research}
        onChange={handleChange}
      />



      <input
        name="count"
        placeholder="Number of personas"
        value={formData.count}
        onChange={handleChange}
      />



      <button 
        onClick={generatePersonas}
        disabled={loading}
      >

        {
          loading 
          ?
          "🤖 Generating AI Personas..."
          :
          "Generate Personas"
        }

      </button>



      {
        loading && (

          <div className="loader">

            AI is creating synthetic users...
            <br/>
            This may take a few seconds.

          </div>

        )
      }



    </div>

  );

}


export default ScenarioCreator;
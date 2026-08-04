function Features() {
  const features = [
    {
      icon: "👥",
      title: "Synthetic User Generation",
      description:
        "Create realistic AI users with different behaviors, preferences, and decision patterns."
    },
    {
      icon: "📝",
      title: "Scenario Creation",
      description:
        "Build custom scenarios and test possible outcomes before making decisions."
    },
    {
      icon: "🤖",
      title: "AI Simulation Engine",
      description:
        "Run powerful AI simulations to predict future results."
    },
    {
      icon: "📊",
      title: "Intelligent Analytics",
      description:
        "Analyze simulation data and get actionable insights."
    }
  ];

  return (
    <section className="features">

      <h2>
        Powerful AI Decision Intelligence
      </h2>

      <div className="feature-grid">

        {features.map((feature, index) => (
          <div className="feature-card" key={index}>

            <div className="feature-icon">
              {feature.icon}
            </div>

            <h3>
              {feature.title}
            </h3>

            <p>
              {feature.description}
            </p>

          </div>
        ))}

      </div>

    </section>
  );
}

export default Features;
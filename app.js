 function sendData() {
      var topic = document.querySelector(".topic").value;
      var number = document.getElementById("customRange2").value;

      fetch("http://localhost:5000/generate_pdf", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          topic: topic,
          number: number,
        }),
      })
        .then((response) => {
          if (response.ok) {

            alert("PDF generated successfully");

            location.reload();
          } else {

            alert("Failed to generate PDF");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
     
          alert("An error occurred");
        });
    };

function slidervalue(value) {
  document.querySelector(".slider_value").textContent = value;
}

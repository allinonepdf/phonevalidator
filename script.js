async function validatePhone() {
  const phone = document.getElementById("phoneInput").value;
  const apiKey = "e2a124b534c2404e935181df56541bec";
  const url = `https://api.apilayer.com/number_verification/validate?number=${phone}`;

  try {
    const response = await fetch(url, {
      headers: {
        "apikey": apiKey
      }
    });

    const data = await response.json();
    let resultDiv = document.getElementById("result");

    if (data.valid) {
      const currentDate = new Date().toLocaleDateString("en-US");

      resultDiv.innerHTML = `
        <strong>Phone Number:</strong> ${data.international_format || data.number}<br>
        <strong>Date of this Report:</strong> ${currentDate}<br>
        <strong>Phone Line Type:</strong> ${data.line_type || "Unknown"}<br>
        <strong>Phone Company:</strong> ${data.carrier || "Unknown"}<br>
        <strong>Phone Location:</strong> ${data.location || "Unknown"}
      `;
    } else {
      resultDiv.innerHTML = "❌ Invalid Phone Number";
    }
  } catch (error) {
    console.error(error);
    document.getElementById("result").innerHTML = "Error validating phone number.";
  }
}

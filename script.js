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
      resultDiv.innerHTML = `
        ✅ Valid Number<br>
        Country: ${data.country_name}<br>
        Line Type: ${data.line_type}
      `;
    } else {
      resultDiv.innerHTML = "❌ Invalid Phone Number";
    }
  } catch (error) {
    console.error(error);
    document.getElementById("result").innerHTML = "Error validating phone number.";
  }
}

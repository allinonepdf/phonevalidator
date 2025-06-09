async function validatePhone() {
  const phone = document.getElementById("phoneInput").value;
  const apiKey = "e2a124b534c2404e935181df56541bec";
  const url = `https://api.apilayer.com/number_verification/validate?number=${phone}`;

  try {
    const res = await fetch(url, {
      headers: {
        "apikey": apiKey
      }
    });
    const data = await res.json();

    if (!data.valid) {
      alert("❌ Invalid phone number.");
      return;
    }

    const infoHTML = `
      <ul>
        <li><strong>Phone Number:</strong> (${data.country_code}) ${data.national_format || data.number}</li>
        <li><strong>Date of this Report:</strong> ${new Date().toLocaleDateString()}</li>
        <li><strong>Phone Line Type:</strong> ${data.line_type || "Unknown"}</li>
        <li><strong>Phone Company:</strong> ${data.carrier || "Unknown"}</li>
        <li><strong>Phone Location:</strong> ${data.location || "Unknown"}</li>
        <li><strong>Owner's Name & Address:</strong> <a href="#" style="color: green">Click Here</a></li>
      </ul>
      <small>Sponsored by PeopleFinders.com</small>
    `;

    document.getElementById("resultInfo").innerHTML = infoHTML;

    const mapHTML = `<iframe
      src="https://maps.google.com/maps?q=${encodeURIComponent(data.location || "USA")}&z=10&output=embed"
      width="300"
      height="200"
      loading="lazy"></iframe>`;
    document.getElementById("mapContainer").innerHTML = mapHTML;

    document.getElementById("outputContainer").classList.remove("hidden");
  } catch (error) {
    alert("Error fetching phone data.");
    console.error(error);
  }
}

function searchAgain() {
  document.getElementById("phoneInput").value = "";
  document.getElementById("outputContainer").classList.add("hidden");
}

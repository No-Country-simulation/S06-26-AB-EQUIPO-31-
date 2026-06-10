const form = document.getElementById("orientar-form");
const output = document.getElementById("output");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());
  payload.lat = Number(payload.lat);
  payload.lng = Number(payload.lng);

  output.textContent = "Consultando orientação...";

  try {
    const response = await fetch("http://localhost:3000/orientar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    output.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    output.textContent = `Erro ao consultar backend: ${error.message}`;
  }
});

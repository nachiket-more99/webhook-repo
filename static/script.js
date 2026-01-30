async function loadEvents() {
  try {
    const res = await fetch("/events");
    const events = await res.json();

    const container = document.getElementById("events");
    container.innerHTML = "";

    events.forEach(e => {
      let text = "";

      if (e.action === "PUSH") {
        text = `"${e.author}" pushed to "${e.to_branch}" on ${e.timestamp}`;
      } else if (e.action === "PULL_REQUEST") {
        text = `"${e.author}" submitted a pull request from "${e.from_branch}" to "${e.to_branch}" on ${e.timestamp}`;
      }

      const div = document.createElement("div");
      div.className = "event";
      div.textContent = text;
      container.appendChild(div);
    });
  } catch (err) {
    console.error("Failed to load events", err);
  }
}

loadEvents();
// setInterval(loadEvents, 15000);
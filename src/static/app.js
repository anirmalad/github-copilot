document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message and existing dropdown options
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p class="availability"><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <button type="button" class="participants-btn">Show participants</button>
          <ul class="participants-list hidden"></ul>
        `;

        activitiesList.appendChild(activityCard);

        const participantsBtn = activityCard.querySelector(".participants-btn");
        const participantsList = activityCard.querySelector(".participants-list");

        const updateParticipantsList = () => {
          participantsList.innerHTML = details.participants.length
            ? details.participants
                .map(
                  (email) =>
                    `<li><span class="participant-email">${email}</span>` +
                    ` <button type="button" class="unregister-btn" data-email="${email}">Unregister</button></li>`
                )
                .join("")
            : "<li>No participants yet.</li>";

          participantsList.querySelectorAll(".unregister-btn").forEach((btn) => {
            btn.addEventListener("click", async () => {
              const email = btn.dataset.email;

              try {
                const response = await fetch(
                  `/activities/${encodeURIComponent(name)}/unregister?email=${encodeURIComponent(email)}`,
                  {
                    method: "POST",
                  }
                );

                const result = await response.json();

                if (response.ok) {
                  details.participants = details.participants.filter((participant) => participant !== email);
                  updateParticipantsList();
                  const availability = details.max_participants - details.participants.length;
                  activityCard.querySelector(".availability").textContent = `Availability: ${availability} spots left`;
                  messageDiv.textContent = result.message;
                  messageDiv.className = "success";
                } else {
                  messageDiv.textContent = result.detail || "An error occurred";
                  messageDiv.className = "error";
                }
              } catch (error) {
                messageDiv.textContent = "Failed to unregister participant. Please try again.";
                messageDiv.className = "error";
                console.error("Error unregistering participant:", error);
              }

              messageDiv.classList.remove("hidden");
              setTimeout(() => {
                messageDiv.classList.add("hidden");
              }, 5000);
            });
          });
        };

        participantsBtn.addEventListener("click", () => {
          if (participantsList.classList.contains("hidden")) {
            updateParticipantsList();
            participantsBtn.textContent = "Hide participants";
            participantsList.classList.remove("hidden");
          } else {
            participantsBtn.textContent = "Show participants";
            participantsList.classList.add("hidden");
          }
        });

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});

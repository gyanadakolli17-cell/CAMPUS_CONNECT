
// Shared navigation and small frontend interactions for Campus Connect.
document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".main-nav");

  if (menuButton && nav) {
    menuButton.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("open");
      menuButton.setAttribute("aria-expanded", String(isOpen));
    });
  }

  // Ask Seniors: question search and filters.
  const search = document.getElementById("questionSearch");
  const category = document.getElementById("questionCategory");
  const status = document.getElementById("questionStatus");
  const filterButton = document.getElementById("filterQuestions");
  const emptyQuestions = document.getElementById("emptyQuestions");
  const questionResultCount = document.getElementById("questionResultCount");
  const questionCards = [...document.querySelectorAll(".question-card")];

  const applyQuestionFilters = () => {
    const term = search ? search.value.trim().toLowerCase() : "";
    let visible = 0;

    questionCards.forEach(card => {
      const matchesText = card.textContent.toLowerCase().includes(term);
      const matchesCategory = !category || category.value === "all" ||
        card.dataset.category === category.value;
      const matchesStatus = !status || status.value === "all" ||
        card.dataset.status === status.value;

      const show = matchesText && matchesCategory && matchesStatus;
      card.classList.toggle("hidden", !show);

      if (show) visible++;
    });

    if (emptyQuestions) {
      emptyQuestions.classList.toggle("hidden", visible !== 0);
    }

    if (questionResultCount) {
      questionResultCount.textContent =
        `${visible} ${visible === 1 ? "question" : "questions"} found`;
    }
  };

  if (search && category && status) {
    filterButton?.addEventListener("click", applyQuestionFilters);
    search.addEventListener("input", applyQuestionFilters);
    category.addEventListener("change", applyQuestionFilters);
    status.addEventListener("change", applyQuestionFilters);
    applyQuestionFilters();
  }

  // Projects: category filter.
  const projectCategory = document.getElementById("projectCategory");

  if (projectCategory) {
    const cards = [...document.querySelectorAll(".project-card")];
    const empty = document.getElementById("emptyProjects");

    projectCategory.addEventListener("change", () => {
      let visible = 0;

      cards.forEach(card => {
        const show = projectCategory.value === "all" ||
          card.dataset.category === projectCategory.value;

        card.classList.toggle("hidden", !show);

        if (show) visible++;
      });

      if (empty) empty.classList.toggle("hidden", visible !== 0);
    });
  }

  // Projects: interest form.
  const interestPanel = document.getElementById("interest-form");
  const interestProject = document.getElementById("interestProject");
  const interestForm = document.getElementById("projectInterestForm");
  const interestFeedback = document.getElementById("interestFeedback");
  const interestButtons = [...document.querySelectorAll(".project-interest-trigger")];

  if (interestPanel && interestProject && interestForm && interestFeedback) {
    const closeButton = document.getElementById("closeInterestForm");

    const setInterestPanelOpen = isOpen => {
      interestPanel.hidden = !isOpen;
      interestButtons.forEach(button =>
        button.setAttribute("aria-expanded", String(isOpen))
      );
    };

    interestButtons.forEach(button => {
      button.addEventListener("click", () => {
        const selectedProject = button.dataset.project;

        const matchingOption = [...interestProject.options].find(
          option => option.textContent.trim() === selectedProject
        );

        if (matchingOption) {
          interestProject.value = matchingOption.value;
        }

        interestFeedback.textContent = "";
        interestFeedback.classList.remove("form-success", "form-error");

        setInterestPanelOpen(true);
        interestPanel.scrollIntoView({ behavior: "smooth", block: "center" });
        document.getElementById("interestName").focus({ preventScroll: true });
      });
    });

    closeButton?.addEventListener("click", () => {
      interestForm.reset();
      interestFeedback.textContent = "";
      interestFeedback.classList.remove("form-success", "form-error");
      setInterestPanelOpen(false);
    });

    interestForm.addEventListener("input", () => {
      interestFeedback.textContent = "";
      interestFeedback.classList.remove("form-success", "form-error");
    });

    interestForm.addEventListener("submit", event => {
      const nameInput = document.getElementById("interestName");
      const messageInput = document.getElementById("interestMessage");

      const name = nameInput.value.trim();
      const message = messageInput.value.trim();

      if (!name) {
        event.preventDefault();
        interestFeedback.textContent = "Please enter your name.";
        interestFeedback.classList.add("form-error");
        nameInput.focus();
        return;
      }

      if (message.length < 10) {
        event.preventDefault();
        interestFeedback.textContent =
          "Please enter at least 10 characters about how you can contribute.";
        interestFeedback.classList.add("form-error");
        messageInput.focus();
        return;
      }
    });
  }

  // Senior directory: search and filters.
  const seniorSearch = document.getElementById("seniorSearch");
  const seniorDepartment = document.getElementById("seniorDepartment");
  const seniorTopic = document.getElementById("seniorTopic");

  if (seniorSearch && seniorDepartment && seniorTopic) {
    const cards = [...document.querySelectorAll(".senior-card")];
    const empty = document.getElementById("emptySeniors");
    const resultCount = document.getElementById("seniorResultCount");

    const applyFilters = () => {
      const term = seniorSearch.value.trim().toLowerCase();
      let visible = 0;

      cards.forEach(card => {
        const matchesText = card.textContent.toLowerCase().includes(term);
        const matchesDepartment = seniorDepartment.value === "all" ||
          card.dataset.department === seniorDepartment.value;
        const matchesTopic = seniorTopic.value === "all" ||
          card.dataset.topic === seniorTopic.value;

        const show = matchesText && matchesDepartment && matchesTopic;
        card.classList.toggle("hidden", !show);

        if (show) visible++;
      });

      if (empty) empty.classList.toggle("hidden", visible !== 0);

      if (resultCount) {
        resultCount.textContent =
          `${visible} ${visible === 1 ? "senior" : "seniors"} found`;
      }
    };

    seniorSearch.addEventListener("input", applyFilters);
    seniorDepartment.addEventListener("change", applyFilters);
    seniorTopic.addEventListener("change", applyFilters);
    applyFilters();
  }
});

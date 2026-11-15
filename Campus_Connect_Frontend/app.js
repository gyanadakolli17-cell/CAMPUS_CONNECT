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

  const search = document.getElementById("questionSearch");
  const category = document.getElementById("questionCategory");
  const status = document.getElementById("questionStatus");
  const filterButton = document.getElementById("filterQuestions");
  const questionList = document.getElementById("questionList");
  const emptyQuestions = document.getElementById("emptyQuestions");
  const questionResultCount = document.getElementById("questionResultCount");
  let questionCards = [...document.querySelectorAll(".question-card")];
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
    if (emptyQuestions) emptyQuestions.classList.toggle("hidden", visible !== 0);
    if (questionResultCount) {
      questionResultCount.textContent = `${visible} ${visible === 1 ? "question" : "questions"} found`;
    }
  };
  if (search && category && status) {
    filterButton?.addEventListener("click", applyQuestionFilters);
    search.addEventListener("input", applyQuestionFilters);
    category.addEventListener("change", applyQuestionFilters);
    status.addEventListener("change", applyQuestionFilters);
  }

  const questionForm = document.getElementById("questionForm");
  if (questionForm && questionList && category) {
    const titleInput = document.getElementById("newQuestionTitle");
    const categoryInput = document.getElementById("questionFormCategory");
    const detailsInput = document.getElementById("newQuestionDetails");
    const feedback = document.getElementById("questionFeedback");
    const categoryStyles = {
      academics: "pill-purple",
      campus: "pill-blue",
      career: "pill-green",
      projects: "pill-orange"
    };

    questionForm.addEventListener("input", () => {
      feedback.textContent = "";
      feedback.classList.remove("form-success", "form-error");
    });

    questionForm.addEventListener("submit", event => {
      event.preventDefault();
      const title = titleInput.value.trim();
      const details = detailsInput.value.trim();
      if (title.length < 8) {
        feedback.textContent = "Please enter a question title with at least 8 characters.";
        feedback.classList.add("form-error");
        titleInput.focus();
        return;
      }
      if (details.length < 20) {
        feedback.textContent = "Please add at least 20 characters of detail.";
        feedback.classList.add("form-error");
        detailsInput.focus();
        return;
      }

      const card = document.createElement("article");
      card.className = "question-card";
      card.dataset.category = categoryInput.value;
      card.dataset.status = "open";

      const top = document.createElement("div");
      top.className = "question-top";
      const categoryBadge = document.createElement("span");
      categoryBadge.className = `pill ${categoryStyles[categoryInput.value] || "pill-blue"}`;
      categoryBadge.textContent = categoryInput.options[categoryInput.selectedIndex].textContent;
      const statusBadge = document.createElement("span");
      statusBadge.className = "status status-open";
      statusBadge.textContent = "Open";
      top.append(categoryBadge, statusBadge);

      const heading = document.createElement("h3");
      heading.textContent = title;
      const description = document.createElement("p");
      description.textContent = details;
      const meta = document.createElement("div");
      meta.className = "question-meta";
      ["◷ Just now", "0 answers", "Asked by you"].forEach(text => {
        const item = document.createElement("span");
        item.textContent = text;
        meta.append(item);
      });
      card.append(top, heading, description, meta);
      questionList.prepend(card);
      questionCards.unshift(card);
      search.value = "";
      category.value = "all";
      status.value = "all";
      applyQuestionFilters();
      questionForm.reset();
      feedback.textContent = "Question added to this page only. It will not be saved or shared.";
      feedback.classList.add("form-success");
    });
  }

  // Projects: category filter.
  const projectCategory = document.getElementById("projectCategory");
  if (projectCategory) {
    const cards = [...document.querySelectorAll(".project-card")];
    const empty = document.getElementById("emptyProjects");
    projectCategory.addEventListener("change", () => {
      let visible = 0;
      cards.forEach(card => {
        const show = projectCategory.value === "all" || card.dataset.category === projectCategory.value;
        card.classList.toggle("hidden", !show);
        if (show) visible++;
      });
      if (empty) empty.classList.toggle("hidden", visible !== 0);
    });
  }

  const interestPanel = document.getElementById("interest-form");
  const interestProject = document.getElementById("interestProject");
  const interestForm = document.getElementById("projectInterestForm");
  const interestFeedback = document.getElementById("interestFeedback");
  const interestButtons = [...document.querySelectorAll(".project-interest-trigger")];
  if (interestPanel && interestProject && interestForm && interestFeedback) {
    const closeButton = document.getElementById("closeInterestForm");
    const setInterestPanelOpen = isOpen => {
      interestPanel.hidden = !isOpen;
      interestButtons.forEach(button => button.setAttribute("aria-expanded", String(isOpen)));
    };

    interestButtons.forEach(button => {
      button.addEventListener("click", () => {
        interestProject.value = button.dataset.project;
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
      event.preventDefault();
      const nameInput = document.getElementById("interestName");
      const messageInput = document.getElementById("interestMessage");
      const name = nameInput.value.trim();
      const message = messageInput.value.trim();
      if (!name) {
        interestFeedback.textContent = "Please enter your name.";
        interestFeedback.classList.add("form-error");
        nameInput.focus();
        return;
      }
      if (message.length < 10) {
        interestFeedback.textContent = "Please enter at least 10 characters about how you can contribute.";
        interestFeedback.classList.add("form-error");
        messageInput.focus();
        return;
      }

      const project = interestProject.value;
      interestForm.reset();
      interestProject.value = project;
      interestFeedback.textContent = `Thanks, ${name}. Your interest in ${project} is confirmed for this demo only; no request was sent or saved.`;
      interestFeedback.classList.add("form-success");
    });
  }

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
        resultCount.textContent = `${visible} ${visible === 1 ? "senior" : "seniors"} found`;
      }
    };
    seniorSearch.addEventListener("input", applyFilters);
    seniorDepartment.addEventListener("change", applyFilters);
    seniorTopic.addEventListener("change", applyFilters);
  }
});

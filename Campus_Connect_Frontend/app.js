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

  // Ask Seniors: search + category + status filters (sample frontend data).
  const search = document.getElementById("questionSearch");
  const category = document.getElementById("questionCategory");
  const status = document.getElementById("questionStatus");
  const filterButton = document.getElementById("filterQuestions");
  if (search && category && status) {
    const cards = [...document.querySelectorAll(".question-card")];
    const empty = document.getElementById("emptyQuestions");
    const applyFilters = () => {
      const term = search.value.trim().toLowerCase();
      let visible = 0;
      cards.forEach(card => {
        const matchesText = card.textContent.toLowerCase().includes(term);
        const matchesCategory = category.value === "all" || card.dataset.category === category.value;
        const matchesStatus = status.value === "all" || card.dataset.status === status.value;
        const show = matchesText && matchesCategory && matchesStatus;
        card.classList.toggle("hidden", !show);
        if (show) visible++;
      });
      if (empty) empty.classList.toggle("hidden", visible !== 0);
    };
    filterButton?.addEventListener("click", applyFilters);
    search.addEventListener("input", applyFilters);
    category.addEventListener("change", applyFilters);
    status.addEventListener("change", applyFilters);
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
});

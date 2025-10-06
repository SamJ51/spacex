document.addEventListener("DOMContentLoaded", function() {
  const searchInput = document.getElementById("query");
  const cards = document.querySelectorAll(".card");

  searchInput.addEventListener("input", function() {
    const searchTerm = this.value.toLowerCase();

    cards.forEach(card => {
      const name = card.querySelector(".card-title")?.textContent.toLowerCase() || "";

      const metaLists = Array.from(card.querySelectorAll(".meta-list, .kv, p"))
        .map(el => el.textContent.toLowerCase())
        .join(" ");

      if (name.includes(searchTerm) || metaLists.includes(searchTerm)) {
        card.style.display = "";
      } else {
        card.style.display = "none";
      }
    });
  });
});
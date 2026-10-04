// Progressive enhancement for the entry tables: sortable columns and a text filter.
// Without JavaScript the tables are plain, sorted by key.
(() => {
  const cellText = (row, i) => row.cells[i].textContent.trim();

  document.querySelectorAll("table.entries").forEach((table) => {
    const body = table.tBodies[0];
    table.querySelectorAll("th[data-sort]").forEach((th) => {
      th.tabIndex = 0;
      const sort = () => {
        const column = th.cellIndex;
        const ascending = th.getAttribute("aria-sort") !== "ascending";
        const rows = [...body.rows];
        const numeric = rows.every((r) => cellText(r, column) === "" || !isNaN(cellText(r, column)));
        rows.sort((a, b) => {
          const [x, y] = [cellText(a, column), cellText(b, column)];
          const order = numeric ? (x === "" ? Infinity : +x) - (y === "" ? Infinity : +y) : x.localeCompare(y, "en", { sensitivity: "base" });
          return ascending ? order : -order;
        });
        rows.forEach((r) => body.append(r));
        table.querySelectorAll("th").forEach((other) => other.removeAttribute("aria-sort"));
        th.setAttribute("aria-sort", ascending ? "ascending" : "descending");
      };
      th.addEventListener("click", sort);
      th.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          sort();
        }
      });
    });
  });

  const input = document.querySelector("input[data-filter-for]");
  if (!input) return;
  const table = document.getElementById(input.dataset.filterFor);
  const output = document.getElementById("filter-count");
  const rows = [...table.tBodies[0].rows];
  const texts = rows.map((r) => r.textContent.toLowerCase());
  const apply = () => {
    const words = input.value.toLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;
    rows.forEach((row, i) => {
      const match = words.every((w) => texts[i].includes(w));
      row.hidden = !match;
      shown += match;
    });
    output.textContent = words.length ? `${shown} of ${rows.length} shown` : "";
  };
  input.addEventListener("input", apply);
  input.value = new URLSearchParams(location.search).get("q") || "";
  apply();
})();

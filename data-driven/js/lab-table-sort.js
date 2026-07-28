(function () {
  function parseNumber(value) {
    var cleaned = value.replace(/[^0-9.-]/g, "");
    if (!cleaned) return Number.NEGATIVE_INFINITY;
    return Number(cleaned);
  }

  document.querySelectorAll(".lab-comparison-table").forEach(function (table) {
    var buttons = table.querySelectorAll(".lab-sort");
    buttons.forEach(function (button, index) {
      button.addEventListener("click", function () {
        var tbody = table.tBodies[0];
        var rows = Array.prototype.slice.call(tbody.rows);
        var direction = button.getAttribute("aria-sort") === "ascending" ? "descending" : "ascending";
        var type = button.dataset.sort || "text";

        buttons.forEach(function (other) {
          other.removeAttribute("aria-sort");
        });
        button.setAttribute("aria-sort", direction);

        rows.sort(function (a, b) {
          var aText = a.cells[index].textContent.trim();
          var bText = b.cells[index].textContent.trim();
          var result = type === "number"
            ? parseNumber(aText) - parseNumber(bText)
            : aText.localeCompare(bText, undefined, { sensitivity: "base" });
          return direction === "ascending" ? result : -result;
        });

        rows.forEach(function (row, rowIndex) {
          row.cells[0].textContent = rowIndex + 1;
          tbody.appendChild(row);
        });
      });
    });
  });
})();

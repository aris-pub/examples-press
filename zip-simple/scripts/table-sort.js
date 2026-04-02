// Minimal sortable table columns
document.querySelectorAll("th").forEach(function (header, index) {
    header.addEventListener("click", function () {
        var table = header.closest("table");
        var tbody = table.querySelector("tbody");
        var rows = Array.from(tbody.querySelectorAll("tr"));
        var ascending = header.dataset.sort !== "asc";

        rows.sort(function (a, b) {
            var aText = a.cells[index].textContent.trim();
            var bText = b.cells[index].textContent.trim();
            var aNum = parseFloat(aText.replace(/,/g, ""));
            var bNum = parseFloat(bText.replace(/,/g, ""));
            if (!isNaN(aNum) && !isNaN(bNum)) {
                return ascending ? aNum - bNum : bNum - aNum;
            }
            return ascending ? aText.localeCompare(bText) : bText.localeCompare(aText);
        });

        rows.forEach(function (row) { tbody.appendChild(row); });
        header.dataset.sort = ascending ? "asc" : "desc";
    });
});

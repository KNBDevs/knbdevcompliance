document.addEventListener("DOMContentLoaded", function () {
  const selector = document.getElementById("fontSizeSelector");
  const html = document.documentElement;

  if (!selector || !html) return;

  const savedSize = localStorage.getItem("fontSize") || "16px";
  html.style.fontSize = savedSize;
  selector.value = savedSize;

  selector.addEventListener("change", function () {
    const newSize = this.value;
    localStorage.setItem("fontSize", newSize);
    html.style.fontSize = newSize;
  });
});

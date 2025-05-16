const modal = document.getElementById("termsModal");
const openBtn = document.getElementById("openModalBtn");
const closeBtn = document.querySelector(".close");
const acceptBtn = document.getElementById("acceptBtn");

openBtn.onclick = () => modal.style.display = "block";
closeBtn.onclick = () => modal.style.display = "none";
acceptBtn.onclick = () => modal.style.display = "none";

window.onclick = event => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
};
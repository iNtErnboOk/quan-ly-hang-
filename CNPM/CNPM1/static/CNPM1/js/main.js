const eyes = document.querySelectorAll(".icon-eye");
const pwds = document.querySelectorAll(".pwd");
eyes.forEach((eye, index) => {
  eye.addEventListener("click", function () {
    const pwd = pwds[index];
    if (pwd.type === "password") {
      pwd.type = "text";
      eye.classList.replace("fa-eye", "fa-eye-slash");
    } else {
      pwd.type = "password";
      eye.classList.replace("fa-eye-slash", "fa-eye");
    }
  });
});

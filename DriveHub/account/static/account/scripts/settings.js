function togglePassword() {
  const field = document.getElementById("id_new_password");
  const VisibleIcon = document.getElementById("visible-eye");
  const NonVisibleIcon = document.getElementById("non-visible-eye");

  if (field.type === "password") {
    field.type = "text";
  } else {
    field.type = "password";
  }
  
  VisibleIcon.classList.toggle("visible");
  NonVisibleIcon.classList.toggle("visible");
}
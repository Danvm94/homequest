//Script to start all Bootstrap Toasts
$(document).ready(function() {
  const toastElList = [].slice.call(document.querySelectorAll('.toast'));
  const toastList = toastElList.map(function(toastEl) {
    return new bootstrap.Toast(toastEl);
  });
  toastList.forEach(toast => toast.show());
});
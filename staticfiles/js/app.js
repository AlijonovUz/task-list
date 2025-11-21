document.addEventListener("DOMContentLoaded", function() {
    const tasks = document.querySelectorAll("[data-deadline]");
    tasks.forEach(task => {
        const deadline = new Date(task.dataset.deadline);
        function updateStatus() {
            const now = new Date();
            if (now > deadline && task.textContent.includes("Kutilmoqda")) {
                task.textContent = "Muddati o'tgan";
                task.classList.remove("badge-gradient-warning");
                task.classList.add("badge-gradient-danger");
            }
        }
        setInterval(updateStatus, 1000);
        updateStatus();
    });
});

setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => new bootstrap.Alert(alert).close());
}, 3000);
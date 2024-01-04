document.addEventListener("DOMContentLoaded", function() {
    const completeButtons = document.querySelectorAll(".complete-btn");
    const deleteButtons = document.querySelectorAll(".delete-btn");
    const restoreButtons = document.querySelectorAll(".restore-btn");
    const importanceSelects = document.querySelectorAll(".importance-select");

    completeButtons.forEach(btn => {
        btn.addEventListener("click", function() {
            const taskId = btn.getAttribute("data-id");
            console.log("Complete button clicked!", taskId);
            completeTask(taskId, btn);
        });
    });

    deleteButtons.forEach(btn => {
        btn.addEventListener("click", function() {
            const taskId = btn.getAttribute("data-id");
            console.log("Delete button clicked!", taskId);
            deleteTask(taskId, btn);
        });
    });

    restoreButtons.forEach(btn => {
        btn.addEventListener("click", function() {
            const taskId = btn.getAttribute("data-id");
            console.log("Restore button clicked!", taskId);
            restoreTask(taskId, btn);
        });
    });

    importanceSelects.forEach(select => {
        select.addEventListener("change", function() {
            const taskId = select.getAttribute("data-id");
            const newImportance = select.value;
            updateTaskImportance(taskId, newImportance, select);
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//this needs some work
function deleteTask(taskId, btn) {
    if (btn.closest('deleted_tasks')) {
        alert('You are about to permanently delete this task.');
        const isConfirmed = window.confirm('Are you sure you want to delete this task permanently?');
        if (!isConfirmed) {
            return; 
        }
    }
    fetch("/tasks/deleting_task/", {
        method: "POST",
        body: new URLSearchParams({ "task_id": taskId }),
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "ok") {
            console.log("Task successfully deleted!");
            const taskElement = btn.closest('tr');
            taskElement.remove();
        } else {
            console.error("Error deleting task:", data.message);
        }
    });
}

function completeTask(taskId) {
    fetch("/tasks/update_task/", {
        method: "POST",
        body: new URLSearchParams({ "task_id": taskId }), 
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "ok") {
            console.log("Task successfully completed!");
        
            let buttonElement = document.querySelector(`button[data-id="${taskId}"]`);
            console.log("Button element found:", buttonElement);
        
            if (buttonElement) {
                let taskRow = buttonElement.closest('tr');
                console.log("Associated row:", taskRow);
        
                if (taskRow) {
                    taskRow.remove();
                    console.log("Row should be removed now.");
                } else {
                    console.error("No tr found for button:", buttonElement);
                }
            } else {
                console.error("Button with taskId not found:", taskId);
            }
        }
    });
}

function restoreTask(taskId, btn) {
    fetch("/tasks/restore_task/", {
        method: "POST",
        body: new URLSearchParams({ "task_id": taskId }),
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "ok") {
            console.log("Task successfully restored!");
            const taskElement = btn.closest('tr');
            taskElement.remove();
        } else {
            console.error("Error restoring task:", data.message);
        }
    });
}

function updateTaskImportance(taskId, newImportance, selectElement) {
    fetch("/tasks/update_importance/", {
        method: "POST",
        body: new URLSearchParams({ "task_id": taskId, "importance": newImportance }),
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "ok") {
            console.log("Task importance updated!");
            const taskRow = selectElement.closest('tr');
            moveTaskToNewSection(taskRow, newImportance);

        } else {
            console.error("Error updating task importance:", data.message);
        }
    });
}

function moveTaskToNewSection(taskRow, newImportance) {
    
    const importanceMapping = {
        "most_important": "most-important-tasks",
        "very_important": "very-important-tasks",
        "important": "important-tasks",
        "not_important": "not-important-tasks"
    };

    taskRow.remove();

    const newSection = document.querySelector(`.${importanceMapping[newImportance]} tbody`);
    newSection.appendChild(taskRow);
}
const API_URL = "http://127.0.0.1:8000"
const taskList = document.getElementById("taskList")

async function loadTasks() {
    const response = await fetch(`${API_URL}/tasks`)
    const tasks = await response.json()

    taskList.innerHTML = ""
    for (const task of tasks) {
        const li = document.createElement("li")
        li.className = "task"
        if (task.done) li.classList.add("done")

        const badge = document.createElement("span")
        badge.className = `badge p${Math.min(task.priority, 3)}`
        badge.textContent = task.priority

        const body = document.createElement("div")
        body.className = "task-body"

        const title = document.createElement("strong")
        title.textContent = task.title

        const description = document.createElement("span")
        description.textContent = task.description ?? ""

        body.append(title, description)
        const actions = document.createElement("div")
        actions.className = "task-actions"

        const doneBtn = document.createElement("button")
        doneBtn.textContent = task.done ? "Undo" : "Done"
        doneBtn.addEventListener("click", async () => {
            await fetch(`${API_URL}/tasks/${task.id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    title: task.title,
                    description: task.description,
                    priority: task.priority,
                    done: !task.done,
                }),
            })
            await loadTasks()
        })

        const deleteBtn = document.createElement("button")
        deleteBtn.className = "delete"
        deleteBtn.textContent = "Delete"
        deleteBtn.addEventListener("click", async () => {
            await fetch(`${API_URL}/tasks/${task.id}`, { method: "DELETE" })
            await loadTasks()
        })

        actions.append(doneBtn, deleteBtn)
        li.append(badge, body, actions)
        taskList.append(li)
    }
}
loadTasks()

const form = document.getElementById("taskForm")
const message = document.getElementById("message")

function showMessage(text) {
    message.textContent = text
    message.hidden = false
}

form.addEventListener("submit", async (event) => {
    event.preventDefault()
    message.hidden = true

    const newTask = {
        title: document.getElementById("taskTitle").value.trim(),
        description: document.getElementById("taskDescription").value.trim() || null,
        priority: Number(document.getElementById("taskPriority").value),
    }

    try {
        const response = await fetch(`${API_URL}/tasks`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newTask),
        })

        if (!response.ok) {
            showMessage("Could not add the task")
            return
        }

        form.reset()
        await loadTasks()
    } catch (error) {
        showMessage("Server is not reachable")
    }
})

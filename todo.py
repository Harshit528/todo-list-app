import streamlit as st
import pandas as pd
from datetime import datetime

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="To-Do List App",
    page_icon="✅",
    layout="centered"
)

# ── Session State (stores tasks) ──────────────────────────────
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ── Helper Functions ──────────────────────────────────────────
def add_task(title, priority, category, due_date):
    st.session_state.tasks.append({
        "id":        len(st.session_state.tasks) + 1,
        "title":     title,
        "priority":  priority,
        "category":  category,
        "due_date":  str(due_date),
        "done":      False,
        "created":   datetime.now().strftime("%Y-%m-%d %H:%M"),
    })

def delete_task(index):
    st.session_state.tasks.pop(index)

def toggle_done(index):
    st.session_state.tasks[index]["done"] = not st.session_state.tasks[index]["done"]

def get_priority_color(priority):
    return {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(priority, "⚪")

# ── UI ────────────────────────────────────────────────────────
st.title("✅ To-Do List App")
st.markdown("Manage your tasks easily — add, complete, and delete tasks.")
st.divider()

# ── Add Task Form ─────────────────────────────────────────────
with st.expander("➕ Add New Task", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        task_title = st.text_input("📝 Task Title", placeholder="e.g. Complete Python project")
        priority   = st.selectbox("🔥 Priority", ["High", "Medium", "Low"])

    with col2:
        category = st.selectbox("📂 Category", ["Work", "Study", "Personal", "Health", "Shopping", "Other"])
        due_date = st.date_input("📅 Due Date", value=datetime.today())

    if st.button("➕ Add Task", use_container_width=True, type="primary"):
        if not task_title.strip():
            st.warning("⚠️ Please enter a task title.")
        else:
            add_task(task_title.strip(), priority, category, due_date)
            st.success(f"✅ Task '{task_title}' added successfully!")
            st.rerun()

st.divider()

# ── Filter & Search ───────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    search      = st.text_input("🔍 Search tasks", placeholder="Search...")
with col2:
    filter_cat  = st.selectbox("📂 Filter Category", ["All", "Work", "Study", "Personal", "Health", "Shopping", "Other"])
with col3:
    filter_status = st.selectbox("📌 Filter Status", ["All", "Pending", "Completed"])

# ── Summary Metrics ───────────────────────────────────────────
total     = len(st.session_state.tasks)
completed = sum(1 for t in st.session_state.tasks if t["done"])
pending   = total - completed

c1, c2, c3 = st.columns(3)
c1.metric("📋 Total Tasks",     total)
c2.metric("✅ Completed",       completed)
c3.metric("⏳ Pending",         pending)

st.divider()

# ── Task List ─────────────────────────────────────────────────
st.subheader("📋 Your Tasks")

tasks = st.session_state.tasks

# Apply filters
filtered = []
for i, task in enumerate(tasks):
    if search and search.lower() not in task["title"].lower():
        continue
    if filter_cat != "All" and task["category"] != filter_cat:
        continue
    if filter_status == "Pending" and task["done"]:
        continue
    if filter_status == "Completed" and not task["done"]:
        continue
    filtered.append((i, task))

if not filtered:
    st.info("📭 No tasks found. Add a new task above!")
else:
    for i, task in filtered:
        col1, col2, col3, col4 = st.columns([0.5, 4, 2, 1])

        with col1:
            done = st.checkbox("", value=task["done"], key=f"done_{i}")
            if done != task["done"]:
                toggle_done(i)
                st.rerun()

        with col2:
            title_style = "~~" if task["done"] else ""
            st.markdown(
                f"{title_style}**{get_priority_color(task['priority'])} {task['title']}**{title_style}  \n"
                f"📂 {task['category']} &nbsp;|&nbsp; 📅 {task['due_date']} &nbsp;|&nbsp; "
                f"🕐 {task['created']}"
            )

        with col3:
            status = "✅ Done" if task["done"] else "⏳ Pending"
            if task["done"]:
                st.success(status)
            else:
                st.warning(status)

        with col4:
            if st.button("🗑️", key=f"del_{i}", help="Delete task"):
                delete_task(i)
                st.rerun()

        st.markdown("---")

# ── Export as CSV ─────────────────────────────────────────────
if st.session_state.tasks:
    st.divider()
    st.subheader("📥 Export Tasks")
    df = pd.DataFrame(st.session_state.tasks)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Tasks as CSV",
        data=csv,
        file_name="tasks.csv",
        mime="text/csv",
        use_container_width=True
    )

# ── Clear All ─────────────────────────────────────────────────
    st.divider()
    if st.button("🗑️ Clear All Tasks", use_container_width=True):
        st.session_state.tasks = []
        st.rerun()

# ── Footer ────────────────────────────────────────────────────
st.divider()
st.caption("Built with Streamlit · Internship Project 🎓")

// Trak API Worker
// Tasks, Habits, Nutrition, Exercise endpoints

export default {
  async fetch(request, env, ctx) {
    const DB = env.DB;
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    // CORS headers
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // Route: /api/tasks
      if (path === "/api/tasks" || path.startsWith("/api/tasks/")) {
        return handleTasks(request, path, corsHeaders, DB);
      }
      // Route: /api/habits
      if (path === "/api/habits" || path.startsWith("/api/habits/")) {
        return handleHabits(request, path, corsHeaders, DB);
      }
      // Route: /api/nutrition
      if (path === "/api/nutrition" || path.startsWith("/api/nutrition/")) {
        return handleNutrition(request, path, corsHeaders, DB);
      }
      // Route: /api/exercise
      if (path === "/api/exercise" || path.startsWith("/api/exercise/")) {
        return handleExercise(request, path, corsHeaders, DB);
      }
      // Route: /api/health
      if (path === "/api/health") {
        return new Response(JSON.stringify({ status: "ok", timestamp: new Date().toISOString() }), {
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }

      return new Response(JSON.stringify({ error: "Not found" }), {
        status: 404,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }
  },
};

// ============== TASKS HANDLER ==============
async function handleTasks(request, path, corsHeaders, DB) {
  const method = request.method;
  const id = path.split("/").pop();

  if (method === "GET") {
    if (id && id !== "tasks") {
      // Get single task
      const result = await DB.prepare("SELECT * FROM tat_tasks WHERE id = ?").bind(id).first();
      return new Response(JSON.stringify(result), {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }
    // Get all tasks
    const result = await DB.prepare("SELECT * FROM tat_tasks ORDER BY due_date ASC").all();
    return new Response(JSON.stringify(result.results), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  if (method === "POST") {
    const body = await request.json();
    const { task_name, category, priority, notes } = body;
    
    const id = "rec" + crypto.randomUUID().slice(0, 10);
    const date_created = new Date().toISOString().split("T")[0];
    const due_date = new Date(Date.now() + category * 24 * 60 * 60 * 1000).toISOString().split("T")[0];

    await DB.prepare(`
      INSERT INTO tat_tasks (id, task_name, category, status, priority, date_created, due_date, notes)
      VALUES (?, ?, ?, 'Not Started', ?, ?, ?, ?)
    `).bind(id, task_name, category, priority || "Medium", date_created, due_date, notes || null).run();

    return new Response(JSON.stringify({ success: true, id }), {
      status: 201,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  if (method === "PUT" && id) {
    const body = await request.json();
    const { status, notes } = body;
    const date_completed = status === "Completed" ? new Date().toISOString().split("T")[0] : null;

    await DB.prepare(`
      UPDATE tat_tasks SET status = ?, notes = ?, date_completed = ?, updated_at = datetime('now')
      WHERE id = ?
    `).bind(status, notes || null, date_completed, id).run();

    return new Response(JSON.stringify({ success: true }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  if (method === "DELETE" && id) {
    await DB.prepare("DELETE FROM tat_tasks WHERE id = ?").bind(id).run();
    return new Response(JSON.stringify({ success: true }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  return new Response(JSON.stringify({ error: "Method not allowed" }), {
    status: 405,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}

// ============== HABITS HANDLER ==============
async function handleHabits(request, path, corsHeaders, DB) {
  const method = request.method;
  const id = path.split("/").pop();

  if (method === "GET") {
    const date = new URL(request.url).searchParams.get("date") || new Date().toISOString().split("T")[0];
    const result = await DB.prepare("SELECT * FROM habits WHERE date = ?").bind(date).all();
    return new Response(JSON.stringify(result.results), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  if (method === "POST") {
    const body = await request.json();
    const { habit_name, date, completed, notes } = body;
    const id = "hab" + crypto.randomUUID().slice(0, 10);
    const today = date || new Date().toISOString().split("T")[0];

    await DB.prepare(`
      INSERT OR REPLACE INTO habits (id, habit_name, date, completed, notes)
      VALUES (?, ?, ?, ?, ?)
    `).bind(id, habit_name, today, completed ? 1 : 0, notes || null).run();

    return new Response(JSON.stringify({ success: true, id }), {
      status: 201,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  return new Response(JSON.stringify({ error: "Method not allowed" }), {
    status: 405,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}

// ============== NUTRITION HANDLER ==============
async function handleNutrition(request, path, corsHeaders, DB) {
  const method = request.method;
  const id = path.split("/").pop();

  if (method === "GET") {
    const date = new URL(request.url).searchParams.get("date") || new Date().toISOString().split("T")[0];
    const result = await DB.prepare("SELECT * FROM nutrition WHERE date = ? ORDER BY created_at DESC").bind(date).all();
    return new Response(JSON.stringify(result.results), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  if (method === "POST") {
    const body = await request.json();
    const { date, meal_type, description, calories, protein, carbs, fat, source } = body;
    const id = "nut" + crypto.randomUUID().slice(0, 10);
    const today = date || new Date().toISOString().split("T")[0];

    await DB.prepare(`
      INSERT INTO nutrition (id, date, meal_type, description, calories, protein, carbs, fat, source)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(id, today, meal_type, description, calories, protein, carbs, fat, source || "manual").run();

    return new Response(JSON.stringify({ success: true, id }), {
      status: 201,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  return new Response(JSON.stringify({ error: "Method not allowed" }), {
    status: 405,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}

// ============== EXERCISE HANDLER ==============
async function handleExercise(request, path, corsHeaders, DB) {
  const method = request.method;
  const id = path.split("/").pop();

  if (method === "GET") {
    const date = new URL(request.url).searchParams.get("date") || new Date().toISOString().split("T")[0];
    const result = await DB.prepare("SELECT * FROM exercise WHERE date = ?").bind(date).all();
    return new Response(JSON.stringify(result.results), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  if (method === "POST") {
    const body = await request.json();
    const { date, workout_type, duration_minutes, strain, notes, source } = body;
    const id = "exe" + crypto.randomUUID().slice(0, 10);
    const today = date || new Date().toISOString().split("T")[0];

    await DB.prepare(`
      INSERT INTO exercise (id, date, workout_type, duration_minutes, strain, notes, source)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `).bind(id, today, workout_type, duration_minutes, strain, notes || null, source || "manual").run();

    return new Response(JSON.stringify({ success: true, id }), {
      status: 201,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  return new Response(JSON.stringify({ error: "Method not allowed" }), {
    status: 405,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}

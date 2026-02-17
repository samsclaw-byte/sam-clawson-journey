// Cloudflare Worker for Work Data Updates
// Handles adding deliverables to TAT Project Deliverables table

export default {
  async fetch(request, env) {
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }
    
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405, headers: corsHeaders });
    }
    
    try {
      const body = await request.json();
      const { action, data } = body;
      
      if (action === 'addDeliverable') {
        return await addDeliverable(data, env, corsHeaders);
      } else if (action === 'updateDeliverable') {
        return await updateDeliverable(data, env, corsHeaders);
      } else if (action === 'updateProjectProgress') {
        return await updateProjectProgress(data, env, corsHeaders);
      }
      
      return new Response('Unknown action', { status: 400, headers: corsHeaders });
      
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};

async function addDeliverable(data, env, corsHeaders) {
  const { name, projectId, status, owner, dueDate, weight, notes } = data;
  
  const airtableUrl = `https://api.airtable.com/v0/${env.AIRTABLE_BASE_ID}/${env.DELIVERABLES_TABLE_ID}`;
  
  const record = {
    fields: {
      Name: name,
      Status: status || 'Not Started',
      Owner: owner || '',
      'Due Date': dueDate || '',
      Weight: weight || 10,
      Progress: 0,
      Notes: notes || ''
    }
  };
  
  const response = await fetch(airtableUrl, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.AIRTABLE_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(record)
  });
  
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Airtable error: ${error}`);
  }
  
  const result = await response.json();
  
  return new Response(JSON.stringify({ 
    success: true, 
    deliverable: {
      id: result.id,
      name: result.fields.Name,
      status: result.fields.Status,
      owner: result.fields.Owner,
      dueDate: result.fields['Due Date'],
      weight: result.fields.Weight,
      progress: result.fields.Progress,
      notes: result.fields.Notes
    }
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

async function updateDeliverable(data, env, corsHeaders) {
  const { id, updates } = data;
  
  const airtableUrl = `https://api.airtable.com/v0/${env.AIRTABLE_BASE_ID}/${env.DELIVERABLES_TABLE_ID}/${id}`;
  
  const record = { fields: {} };
  if (updates.status) record.fields.Status = updates.status;
  if (updates.progress !== undefined) record.fields.Progress = updates.progress;
  if (updates.owner) record.fields.Owner = updates.owner;
  if (updates.dueDate) record.fields['Due Date'] = updates.dueDate;
  if (updates.notes) record.fields.Notes = updates.notes;
  if (updates.blockedReason) record.fields['Blocked Reason'] = updates.blockedReason;
  
  const response = await fetch(airtableUrl, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${env.AIRTABLE_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(record)
  });
  
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Airtable error: ${error}`);
  }
  
  return new Response(JSON.stringify({ success: true }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

async function updateProjectProgress(data, env, corsHeaders) {
  const { projectId, progress } = data;
  
  const airtableUrl = `https://api.airtable.com/v0/${env.AIRTABLE_BASE_ID}/${env.PROJECTS_TABLE_ID}/${projectId}`;
  
  const response = await fetch(airtableUrl, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${env.AIRTABLE_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      fields: { Progress: progress }
    })
  });
  
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Airtable error: ${error}`);
  }
  
  return new Response(JSON.stringify({ success: true }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

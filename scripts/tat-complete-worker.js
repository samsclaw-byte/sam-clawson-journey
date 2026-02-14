// Cloudflare Worker for TAT Task Completion
// This worker receives requests from Mission Control and updates Airtable

export default {
  async fetch(request, env) {
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
      });
    }

    // Only accept POST requests
    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'Method not allowed' }), {
        status: 405,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });
    }

    try {
      // Parse request body
      const body = await request.json();
      const { taskId, status } = body;

      // Validate inputs
      if (!taskId || !status) {
        return new Response(JSON.stringify({ error: 'Missing taskId or status' }), {
          status: 400,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        });
      }

      // Validate status value
      const validStatuses = ['Not Started', 'In Progress', 'Blocked', 'Complete'];
      if (!validStatuses.includes(status)) {
        return new Response(JSON.stringify({ error: 'Invalid status value' }), {
          status: 400,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        });
      }

      // Get Airtable credentials from environment
      const airtableKey = env.AIRTABLE_API_KEY;
      const baseId = env.AIRTABLE_BASE_ID || 'appvUbV8IeGhxmcPn';
      const tableId = env.AIRTABLE_TABLE_ID || 'tblkbuvkZUSpm1IgJ';

      if (!airtableKey) {
        return new Response(JSON.stringify({ error: 'Airtable API key not configured' }), {
          status: 500,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        });
      }

      // Update task in Airtable
      const updateUrl = `https://api.airtable.com/v0/${baseId}/${tableId}/${taskId}`;
      const updateResponse = await fetch(updateUrl, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${airtableKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fields: {
            'Status': status,
          },
        }),
      });

      if (!updateResponse.ok) {
        const errorData = await updateResponse.text();
        return new Response(JSON.stringify({ error: 'Airtable API error', details: errorData }), {
          status: 500,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        });
      }

      const updatedTask = await updateResponse.json();

      return new Response(JSON.stringify({
        success: true,
        message: `Task ${taskId} updated to ${status}`,
        task: updatedTask,
      }), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });

    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });
    }
  },
};

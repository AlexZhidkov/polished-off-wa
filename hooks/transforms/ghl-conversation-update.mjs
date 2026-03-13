const GHL_BASE_URL = "https://services.leadconnectorhq.com";
const GHL_VERSION = "2021-04-15";

function pickString(value) {
  return typeof value === "string" && value.trim() ? value.trim() : undefined;
}

function extractConversationId(payload) {
  if (!payload || typeof payload !== "object") {
    return undefined;
  }

  const direct = pickString(payload.conversationId);
  if (direct) {
    return direct;
  }

  const snake = pickString(payload.conversation_id);
  if (snake) {
    return snake;
  }

  const nested = payload.conversation;
  if (nested && typeof nested === "object") {
    const nestedId = pickString(nested.id) || pickString(nested.conversationId);
    if (nestedId) {
      return nestedId;
    }
  }

  return undefined;
}

function extractContactId(payload) {
  if (!payload || typeof payload !== "object") {
    return undefined;
  }

  return (
    pickString(payload.contact_id) ||
    pickString(payload.contactId) ||
    pickString(payload.id)
  );
}

function extractBestConversationId(searchResponse) {
  const rows = Array.isArray(searchResponse?.conversations)
    ? searchResponse.conversations
    : [];

  for (const row of rows) {
    if (!row || typeof row !== "object") {
      continue;
    }
    const id =
      pickString(row.id) ||
      pickString(row.conversationId) ||
      pickString(row._id) ||
      pickString(row.conversation?.id);
    if (id) {
      return id;
    }
  }

  return undefined;
}

function buildMessage(ctx, conversationId, lookupNote) {
  const payload = ctx.payload || {};
  const headers = ctx.headers || {};

  const lines = [
    "REPLY_TO_GHL_CONVERSATION webhook",
    `Received: ${new Date().toISOString()}`,
    `Request ID: ${pickString(headers["x-request-id"]) || ""}`,
    "",
    "Context",
    `- conversationId: ${conversationId || ""}`,
    `- contact_id: ${pickString(payload.contact_id) || ""}`,
    lookupNote ? `- lookup: ${lookupNote}` : "",
    "",
    "Contact",
    `- Contact ID: ${pickString(payload.contact_id) || ""}`,
    `- Full Name: ${pickString(payload.full_name) || ""}`,
    `- Email: ${pickString(payload.email) || ""}`,
    `- Tags: ${pickString(payload.tags) || ""}`,
    "",
    "Form Data",
    `- Message: ${pickString(payload.Message) || ""}`,
    `- When required: ${pickString(payload["When required"]) || ""}`,
    `- Job Size: ${pickString(payload["Job Size"]) || ""}`,
    "",
    "Lead Meta",
    `- Contact Source: ${pickString(payload.contact_source) || ""}`,
    `- Date Created: ${pickString(payload.date_created) || ""}`,
    `- Full Address: ${pickString(payload.full_address) || ""}`,
    "",
    "Instruction",
    "Use the ghl-conversation-processor skill to draft a concise, context-aware follow-up reply and MUST post it by executing /usr/bin/python3 /home/alex/.openclaw/workspace/skills/ghl-conversation-processor/scripts/post_ghl_comment.py with contact_id. Return postResult=posted only on successful API response; otherwise return postResult=failed with postError.",
  ];

  return lines.filter((line) => line !== "").join("\n");
}

export default async function transform(ctx) {
  const payload = ctx.payload || {};
  let conversationId = extractConversationId(payload);
  let lookupNote = "from_payload";

  if (!conversationId) {
    const contactId = extractContactId(payload);
    const token = pickString(process.env.GHL_API_TOKEN);
    const locationId = pickString(process.env.GHL_LOCATION_ID);

    if (contactId && token && locationId) {
      try {
        const searchUrl = new URL(`${GHL_BASE_URL}/conversations/search`);
        searchUrl.searchParams.set("locationId", locationId);
        searchUrl.searchParams.set("contactId", contactId);
        searchUrl.searchParams.set("limit", "5");
        searchUrl.searchParams.set("sort", "desc");

        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 8000);
        const response = await fetch(searchUrl, {
          method: "GET",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${token}`,
            Version: GHL_VERSION,
          },
          signal: controller.signal,
        });
        clearTimeout(timeout);

        if (response.ok) {
          const json = await response.json();
          conversationId = extractBestConversationId(json);
          lookupNote = conversationId
            ? "resolved_by_contact_id"
            : "contact_lookup_no_match";
        } else {
          lookupNote = `contact_lookup_http_${response.status}`;
        }
      } catch {
        lookupNote = "contact_lookup_failed";
      }
    } else {
      lookupNote = "contact_lookup_not_configured";
    }
  }

  return {
    kind: "agent",
    message: buildMessage(ctx, conversationId, lookupNote),
  };
}

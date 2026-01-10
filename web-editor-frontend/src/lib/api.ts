type ApiEnvelope<T> = {
  ok: boolean;
  data: T | null;
  error: { code: string; message: string; details?: Record<string, unknown> } | null;
};

export type ConvertResponse = {
  sourceFormat: string;
  output: { type: 'html' | 'text'; html?: string | null; text: string };
  metadata: { pageCount: number | null };
  warnings: string[];
};

function apiBaseUrl(): string {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!base) throw new Error('NEXT_PUBLIC_API_BASE_URL is not set');
  return base.replace(/\/$/, '');
}

export async function convertDocument(file: File): Promise<ConvertResponse> {
  const form = new FormData();
  form.append('file', file);

  const res = await fetch(`${apiBaseUrl()}/api/convert`, {
    method: 'POST',
    body: form
  });

  const body = (await res.json()) as ApiEnvelope<ConvertResponse>;

  if (!res.ok || !body.ok || !body.data) {
    const msg = body?.error?.message ?? `API error (${res.status})`;
    throw new Error(msg);
  }

  return body.data;
}

'use client';

import { Box, Button, CircularProgress, Paper, Stack, Typography } from '@mui/material';
import { useMemo, useState } from 'react';

import { convertDocument } from '@/lib/api';
import { sanitizeHtml } from '@/lib/sanitizeHtml';
import { RichTextEditor } from '@/components/RichTextEditor';

export function UploadConvert() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [warnings, setWarnings] = useState<string[]>([]);
  const [contentHtml, setContentHtml] = useState<string>('');

  const fileLabel = useMemo(() => file?.name ?? '선택된 파일 없음', [file]);

  async function onConvert() {
    if (!file) return;
    setLoading(true);
    setError(null);
    setWarnings([]);
    try {
      const res = await convertDocument(file);
      const html = res.output.html ?? `<pre>${res.output.text ?? ''}</pre>`;
      setWarnings(res.warnings ?? []);
      setContentHtml(sanitizeHtml(html));
    } catch (e) {
      setError(e instanceof Error ? e.message : '변환 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <Stack spacing={2}>
      <Paper sx={{ p: 2 }} variant="outlined">
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} alignItems={{ sm: 'center' }}>
          <Button component="label" variant="contained">
            파일 선택
            <input
              type="file"
              hidden
              onChange={(e) => {
                const selected = e.target.files?.[0] ?? null;
                setFile(selected);
              }}
            />
          </Button>
          <Typography variant="body2" sx={{ flex: 1 }}>
            {fileLabel}
          </Typography>
          <Button variant="outlined" disabled={!file || loading} onClick={onConvert}>
            변환
          </Button>
          {loading ? <CircularProgress size={22} /> : null}
        </Stack>

        {error ? (
          <Typography color="error" variant="body2" sx={{ mt: 1 }}>
            {error}
          </Typography>
        ) : null}

        {warnings.length ? (
          <Box sx={{ mt: 1 }}>
            {warnings.map((w, idx) => (
              <Typography key={idx} color="warning.main" variant="body2">
                - {w}
              </Typography>
            ))}
          </Box>
        ) : null}
      </Paper>

      <RichTextEditor html={contentHtml} />
    </Stack>
  );
}

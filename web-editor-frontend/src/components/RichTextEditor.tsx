'use client';

import { Box, Paper, Stack, Typography } from '@mui/material';
import { EditorContent, useEditor } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import { useEffect } from 'react';

export function RichTextEditor({ html }: { html: string }) {
  const editor = useEditor({
    extensions: [StarterKit],
    content: html || '<p>여기에 변환 결과가 표시됩니다.</p>'
  });

  useEffect(() => {
    if (!editor) return;
    if (!html) return;
    editor.commands.setContent(html, false);
  }, [editor, html]);

  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Stack spacing={1}>
        <Typography variant="subtitle2">Editor</Typography>
        <Box
          sx={(theme) => ({
            border: `1px solid ${theme.palette.divider}`,
            borderRadius: 1,
            p: 2,
            minHeight: 360,
            '& .ProseMirror': {
              outline: 'none'
            }
          })}
        >
          <EditorContent editor={editor} />
        </Box>
      </Stack>
    </Paper>
  );
}

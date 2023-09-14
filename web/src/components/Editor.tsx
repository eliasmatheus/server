import { useRef } from 'react';
import { Editor } from '@tinymce/tinymce-react';

interface EditorProps {
  id?: string;
  name: string;
  onChange: (value: string) => void;
  onBlur: (value: any) => void;
  value: string;
  isDirty: boolean;
}

export default function App({ id, onChange, isDirty, value, name, onBlur }: EditorProps) {
  const editorRef = useRef(null);

  return (
    <>
      <Editor
        id={id}
        textareaName={name}
        apiKey="your-api-key"
        value={value}
        onInit={(evt, editor) => (editorRef.current = editor)}
        init={{
          height: 500,
          menubar: false,
          plugins: [
            'advlist',
            'autolink',
            'lists',
            'link',
            'image',
            'charmap',
            'preview',
            'anchor',
            'searchreplace',
            'visualblocks',
            'fullscreen',
            'insertdatetime',
            'media',
            'table',
            'help',
            'wordcount',
            'codesample',
          ],
          image_class_list: [
            {
              title: 'Default',
              value: 'rounded-2xl ring-1 ring-inset ring-slate-900/10 dark:ring-white/10',
            },
          ],
          toolbar:
            'undo redo | blocks | ' +
            'bold italic forecolor | alignleft aligncenter ' +
            'alignright alignjustify | bullist numlist outdent indent | ' +
            'image | codesample | removeformat | help',
          content_style:
            'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }',
          placeholder: 'Unleash your inner wordsmith and let your creativity run wild!',
          file_picker_types: 'image media',
        }}
        onEditorChange={newValue => {
          onChange(newValue);
        }}
        onBlur={event => onBlur(event)}
      />
    </>
  );
}

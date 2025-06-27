import React, { useEffect, useRef } from 'react';

const TextArea = ({ formData, handleInputChange, readOnly = false }) => {
    const textAreaRef = useRef(null);

    useEffect(() => {
        if (!readOnly) {
            const handleInput = () => {
                const textarea = textAreaRef.current;
                textarea.style.height = 'auto';
                textarea.style.height = `${textarea.scrollHeight}px`;
            };

            const textarea = textAreaRef.current;
            textarea.addEventListener('input', handleInput);

            return () => {
                textarea.removeEventListener('input', handleInput);
            };
        }
    }, [readOnly]);

    return (
        <textarea
            name="content"
            id="paste"
            ref={textAreaRef}
            value={formData.content}
            onChange={readOnly ? undefined : handleInputChange}
            readOnly={readOnly}
            style={{
                backgroundColor: readOnly ? '#f5f5f5' : 'white',
                border: '1px solid #ccc',
                resize: 'none',
                cursor: readOnly ? 'default' : 'text',
            }}
        />
    );
};

export default TextArea;

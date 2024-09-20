import React, { useEffect, useRef} from 'react'
const TextArea = ({ formData, handleInputChange }) => {
    const textAreaRef = useRef(null);

    useEffect(() => {
        const handleInput = () => {
          const textarea = textAreaRef.current;
          textarea.style.height = 'auto'; // сброс высоты
          textarea.style.height = `${textarea.scrollHeight}px`; // установка новой высоты
        };
    
        const textarea = textAreaRef.current;
        textarea.addEventListener('input', handleInput);
    
        return () => {
          textarea.removeEventListener('input', handleInput);
        };
    }, []);

    return (
        <textarea name="content" id="paste" ref={textAreaRef}
        value={formData.content}
      onChange={handleInputChange}></textarea>
    )
}

export default TextArea
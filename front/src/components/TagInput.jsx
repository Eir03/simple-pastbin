import React from 'react'
import './TagInput.css'

const TagInput = ({tags, onChange}) => {
    const [tagData, setTagData] = React.useState(tags);

    const removeTagData = (indexToRemove) => {
      const newTags = [...tagData.filter((_, index) => index !== indexToRemove)];
      setTagData(newTags);
      onChange(newTags);
    };

    const addTagData = (event) => {
      const newTag = event.target.value.trim();
      if (newTag !== '' && !tagData.includes(newTag) && tagData.length < 15) {
        const newTags = [...tagData, newTag];
        setTagData(newTags);
        onChange(newTags);
        event.target.value = '';
      }
    };

    return (
    <div className="tag-input">
      <input
        type="text"
        onKeyUp={(event) => (event.key === 'Enter' ? addTagData(event) : null)}
      />
      {tagData.length > 0 && (
        <ul className="tags">
          {tagData.map((tag, index) => (
            <li key={index} className="tag">
              <span className="tag-title">{tag}</span>
              <span
                className="tag-close-icon"
                onClick={() => removeTagData(index)}
              >
                ×
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
    )
}

export default TagInput
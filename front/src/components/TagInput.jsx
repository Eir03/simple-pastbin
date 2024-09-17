import React from 'react'
import './TagInput.css'

const TagInput = ({tags}) => {
    const [tagData, setTagData] = React.useState(tags);
    const removeTagData = indexToRemove => {
      setTagData([...tagData.filter((_, index) => index !== indexToRemove)]);
    };
    const addTagData = event => {
        const newTag = event.target.value.trim();
        if (newTag !== '' && !tagData.includes(newTag) && tagData.length < 15) {
          setTagData([...tagData, newTag]);
          event.target.value = '';
        } 
        else if (tagData.includes(newTag)) { return} 
        else if (tagData.length >= 15) { return}
    };
    return (
      <div className="tag-input">
        <input
          type="text"
          onKeyUp={event => (event.key === 'Enter' ? addTagData(event) : null)}
        />
        <ul className="tags">
          {tagData.map((tag, index) => (
            <li key={index} className="tag">
              <span className="tag-title">{tag}</span>
              <span
                className="tag-close-icon"
                onClick={() => removeTagData(index)}>
                ×
              </span>
            </li>
          ))}
        </ul>
        
      </div>
    )
}

export default TagInput
import React, { useEffect, useRef, useState, response } from 'react'
import './Body.css'
import TagInput from './TagInput'
import {createPost} from '../Api';
import TextArea from './TextArea';

const Body = () => {  

  const [fieldConfig, setFieldConfig] = useState([]);

  useEffect(() => {
    const fetchFieldConfig = () => {
      setFieldConfig(temporaryFieldConfig);
    };
    fetchFieldConfig();
  }, []);

  const [formData, setFormData] = useState({
    user_id: NaN,
    title: '',
    content: '',
    category_id: 1,
    is_public: 'Публичный',
    delete_after_reading: false,
    expires_at: '',
    tags: [],
  });
  const handleInputChange = (event) => {
    const { name, value, type, checked } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleTagsChange = (tags) => {
    setFormData((prevData) => ({
      ...prevData,
      tags,
    }));
  };

  const calculateExpirationDate = (time) => {
    const currentDate = new Date();
    if (time === '1 час') {
      currentDate.setHours(currentDate.getHours() + 1);
    } else if (time === '1 день') {
      currentDate.setDate(currentDate.getDate() + 1);
    }
    return currentDate.toISOString();  // Возвращаем строку в формате ISO для базы данных
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const postData = {
      ...formData,
      is_public: formData.is_public === 'Публичный', 
      expires_at: formData.expires_at !== 'Нет' ? calculateExpirationDate(formData.expires_at) : null,
    };

    try {
      const data = await createPost(postData);  // Используем функцию из api.js
      console.log('Ответ сервера:', data);
    } catch (error) {
      console.error('Ошибка при создании поста:', error);
    }
  };
  
  // "category_id": 1,
  // "title": "string",
  // "content": "string",
  // "is_public": true,
  // "delete_after_reading": false,
  // "tags": [
  //   "string"
  // ],
  // "expires_at": "2024-09-19T18:26:45.441Z"

    
  return (
    <form onSubmit={handleSubmit} id='0' className='create-form'
    onKeyDown={(e) => {
      if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
        e.preventDefault();  // Предотвращаем отправку формы, если нажат Enter, кроме поля textarea
      }}}>
      <div className="main">
          <div className="content">
              <h3 className="newpost">Новая заметка</h3>
              <TextArea formData={formData} handleInputChange={handleInputChange}/>
              <div className="settings">
                  <div className="settings_title">
                      <h3>Дополнительные настройки</h3>
                  </div>
                  <div className="settings_body">
                      {fieldConfig.length > 0 ? (
                        fieldConfig.map((field, index) => <FormField key={index} field={field} formData={formData} handleInputChange={handleInputChange} handleTagsChange={handleTagsChange}/>)
                      ) : (
                        <p>Загрузка</p>
                      )}
                      <button className="create-button" type='submit'>Создать новую заметку</button>
                  </div>
              </div>
          </div>
          <div className="sidebar">
              <div className="sidebar_title">
                  <h3>Популярные заметки</h3>
              </div>
              <div className="sidebar_menu">
                  <p><a href="">Популярная заметка</a></p>
                  <p><a href="">Популярная заметка</a></p>
                  <p><a href="">Популярная заметка</a></p>
                  <p><a href="">Популярная заметка</a></p>
                  <p><a href="">Популярная заметка</a></p>
              </div>
          </div> 
      </div>
    </form>
  )
}

const temporaryFieldConfig = [
  {
    label: 'Категория',
    type: 'select',
    name: 'category_id',
    options: ["Отутствует", "Автомобили", "Бизнес", "Дом и сад", "Еда и напитки", "Животные", "Игры", "Искусство", "История", "Книги", "Личное развитие", "Мода", "Музыка", "Наука", "Образование", "Психология", "Путешествия", "Развлечения", "Спорт", "Технологии", "Фильмы", "Финансы", "Фотография", "Политика", "Здоровье"],
  },
  {
    label: 'Метки',
    type: 'tags',
    name: 'tags',
  },
  {
    label: 'Время жизни',
    type: 'select',
    name: 'expires_at',
    options: ['Нет', '1 час', '1 день'],
  },
  {
    label: 'Доступ',
    type: 'select',
    name:'is_public',
    options: ['Публичный', 'Приватный'],
  },
  {
    label: 'Удалить после прочтения',
    type: 'checkbox',
    name: 'delete_after_reading',
    isNew: true,
  },
  {
    label: 'Заголовок',
    type: 'text',
    name: 'title'
  },
];

const FormField = ({ field, formData, handleInputChange, handleTagsChange }) => {
  switch (field.type) {
    case 'select':
      return (
        <div className="form-group">
          <label>{field.label}:</label>
          <select value={formData[field.name]} name={field.name}
            onChange={handleInputChange}>
            {field.options.map((option, index) => (
              <option key={index} value={index + 1}>
                {option}
              </option>
            ))}
          </select>
        </div>
      );
    case 'text':
      return (
        <div className="form-group">
          <label>{field.label}:</label>
          <input type="text"
                      name={field.name}
                      value={formData[field.name]}
                      onChange={handleInputChange}/>
        </div>
      );
    case 'tags':
      return (
        <div className="form-group">
          <label>{field.label}:</label>
          <TagInput tags={[]} onChange={handleTagsChange}/>
        </div>
      );
    case 'checkbox':
      return (
        <div className="form-group">
          <label className='noselect'>
            <input type="checkbox" name={field.name}
              checked={formData[field.name]}
              onChange={handleInputChange}/>
            {field.label}
            {field.isNew && <span className="new-badge">NEW</span>}
          </label>
        </div>
      );
    default:
      return null;
  }
};


export default Body
import React, { useEffect, useRef, useState } from 'react'
import './Body.css'
const temporaryFieldConfig = [
  {
    label: 'Категория',
    type: 'select',
    options: ["Отутствует", "Автомобили", "Бизнес", "Дом и сад", "Еда и напитки", "Животные", "Игры", "Искусство", "История", "Книги", "Личное развитие", "Мода", "Музыка", "Наука", "Образование", "Психология", "Путешествия", "Развлечения", "Спорт", "Технологии", "Фильмы", "Финансы", "Фотография", "Политика", "Здоровье"],
  },
  {
    label: 'Метки',
    type: 'text',
  },
  {
    label: 'Время жизни',
    type: 'select',
    options: ['Нет', '1 час', '1 день'],
  },
  {
    label: 'Доступ',
    type: 'select',
    options: ['Публичный', 'Приватный'],
  },
  {
    label: 'Удалить после прочтения',
    type: 'checkbox',
    isNew: true,
  },
  {
    label: 'Заголовок',
    type: 'text',
  },
];

const FormField = ({ field }) => {
  switch (field.type) {
    case 'select':
      return (
        <div className="form-group">
          <label>{field.label}:</label>
          <select>
            {field.options.map((option, index) => (
              <option key={index} value={option}>
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
          <input type="text" />
        </div>
      );
    case 'checkbox':
      return (
        <div className="form-group">
          <label>
            <input type="checkbox" />
            {field.label}
            {field.isNew && <span className="new-badge">NEW</span>}
          </label>
        </div>
      );
    default:
      return null;
  }
};

const Body = () => {
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

    const [fieldConfig, setFieldConfig] = useState([]);

    useEffect(() => {
      // Заглушка для имитации запроса к API
      const fetchFieldConfig = () => {
        // Задержка для имитации сетевого запроса
        setTimeout(() => {
          setFieldConfig(temporaryFieldConfig);
        }, 500); // 0.5 секунд задержки
      };
  
      fetchFieldConfig();
    }, []);
  return (
    <div className="main">
        <div className="content">
            <h3 className="newpost">Новый пост</h3>
            <textarea name="paste" id="paste" ref={textAreaRef}></textarea>
            <div className="settings">
                <div className="settings_title">
                    <h3>Дополнительные настройки</h3>
                </div>
                <div className="settings_body">
                    {fieldConfig.length > 0 ? (
                      fieldConfig.map((field, index) => <FormField key={index} field={field} />)
                    ) : (
                      <p>Загрузка</p>
                    )}
                    <button className="create-button">Создать новую заметку</button>
                </div>
            </div>
        </div>
        <div className="sidebar">
            <div className="sidebar_title">
                <h3>Популярные посты</h3>
            </div>
            <div className="sidebar_menu">
                <h4>Популярный пост</h4>
                <h4>Популярный пост</h4>
                <h4>Популярный пост</h4>
                <h4>Популярный пост</h4>
                <h4>Популярный пост</h4>
            </div>

        </div> 
    </div>
  )
}

export default Body
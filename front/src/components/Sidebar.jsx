import React from 'react'
import './Sidebar.css'
import {readPosts} from '../Api';
import { useEffect, useState } from 'react'

const Sidebar = () => {
    const [sidebarItems, setSidebarItems] = useState([]);
    const sidebar_item = async (event) => {
        try {
          const data = await readPosts();
          setSidebarItems(data);
        } catch (error) {
          console.error('Ошибка при создании поста:', error);
        }
      };

      useEffect(() => {
        sidebar_item();  // Можно вызвать функцию при монтировании компонента
    }, []);

    return (
        <div className="sidebar">
            <div className="sidebar_title">
                <h3>Популярные заметки</h3>
            </div>
            <div className="sidebar_menu">
                {sidebarItems.length > 0 ? (
                    sidebarItems.map((note) => (
                        <p key={note.id}>
                            <a href={`/${note.hash}`}>{note.title}</a>
                        </p>
                    ))
                ) : (
                    <p>Загрузка...</p>
                )}
            </div>
        </div> 
    )
}

export default Sidebar
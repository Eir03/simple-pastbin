import axios from 'axios';

// Функция для отправки данных формы
export const createPost = async (formData) => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/posts', formData);
    return response.data;
  } catch (error) {
    console.error('Ошибка при отправке:', error);
    throw error;
  }
};

export const readPosts = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/posts');
    return response.data;
  } catch (error) {
    console.error('Ошибка при отправке:', error);
    throw error;
  }
};

import axios from 'axios';

// Функция для отправки данных формы
export const createPost = async (formData) => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/posts', formData);
    console.log('Успешно отправлено:', response.data);
    return response.data;
  } catch (error) {
    console.error('Ошибка при отправке:', error);
    throw error;
  }
};

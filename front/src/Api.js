import axios from 'axios';


const apiUrl = process.env.REACT_APP_API_URL?.replace(/\/$/, '');

// Функция для отправки данных формы
export const createPost = async (formData) => {
  try {
    const response = await axios.post(apiUrl + '/posts', formData);
    return response.data;
  } catch (error) {
    console.error('Ошибка при отправке:', error);
    throw error;
  }
};

export const readPosts = async () => {
  try {
    const response = await axios.get(apiUrl + '/posts');
    return response.data;
  } catch (error) {
    console.error('Ошибка при отправке:', error);
    throw error;
  }
};
